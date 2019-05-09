import string
from datetime import timedelta
from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Prefetch, Value, BooleanField, Count, Q
from django.utils import timezone
from django.utils.crypto import random
from django.views.decorators.csrf import csrf_exempt
from elasticsearch_dsl import Search
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *
from classification.elasticsearch.elasticsearch import ElasticsearchWrapper
from classification.models import UserManualClassification
from restaurants.models import Cousine
from user.models import User, Recommender, UserRecommendationLocation, Friendship
from user.recommendations.saver import RecommendationSaver


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.prefetch_related(
        Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date())),
    )
    serializer_class = RestaurantWithMenuSerializer

    def get_queryset(self):
        user_id = 0
        if self.request.user is not AnonymousUser:
            user_id = self.request.user.id

        qs = self.queryset.prefetch_related(
            Prefetch('daily_menu__dailymenurating_set', queryset=DailyMenuRating.objects.filter(user__pk=user_id))
        )
        return qs


class RestaurantsWithTodayMenuViewSet(RestaurantViewSet):
    """ Get restaurants with todays menu"""
    queryset = Restaurant.objects.prefetch_related(
        Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date())),
    ).filter(
        id__in=DailyMenu.objects.filter(day=timezone.now().date()).values('restaurant_id')
    ).order_by('-rating', 'name')

    serializer_class = RestaurantWithMenuSerializer

    def list(self, request, *args, **kwargs):
        data = request.query_params

        # filter by location
        latitude = float(data['lat']) if 'lat' in data else None
        longitude = float(data['lng']) if 'lng' in data else None

        if latitude is not None and longitude is not None:
            radius = 0.01  # radius cca 2km
            self.queryset = self.queryset.filter(
                gps_lat__isnull=False,
                gps_lng__isnull=False,
                gps_lat__gte=latitude - radius,
                gps_lat__lte=latitude + radius,
                gps_lng__gte=longitude - radius,
                gps_lng__lte=longitude + radius,
            )

        return super().list(request, *args, **kwargs)


class SearchView(RestaurantViewSet):
    queryset = Restaurant.objects
    serializer_class = RestaurantWithMenuSerializer
    pagination_class = None
    es = None

    def get_daily_menu_ids(self, term):
        daily_menus = Search(using=self.es).index("daily_menu").query(
            'multi_match',
            fields=['name', 'tags'],
            query=term,
            fuzziness=1,
            minimum_should_match="2<75%"
        ).filter(
            'match',
            day=timezone.now().date()
        )

        daily_menu_ids = [hit.id for hit in daily_menus]

        return daily_menu_ids

    def search_restaurants(self, term):
        restaurants = Search(using=self.es).index("restaurants").query(
            'multi_match',
            fields=['name'],
            query=term,
            fuzziness=1,
            # minimum_should_match="2<75%"
        )

        restaurant_ids = [hit.id for hit in restaurants]

        return restaurant_ids

    def get_queryset(self):
        if 'q' not in self.request.query_params:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        self.es = ElasticsearchWrapper().client

        term = self.request.query_params['q']
        daily_menus_ids = self.get_daily_menu_ids(term)
        restaurant_ids = self.search_restaurants(term)

        subselect = DailyMenu.objects.filter(pk__in=daily_menus_ids)
        daily_menus_results = Restaurant.objects.prefetch_related(
            Prefetch('daily_menu', queryset=subselect),
        ).filter(
            Q(id__in=subselect.values('restaurant_id'))
        )
        restaurants_results = Restaurant.objects.filter(Q(pk__in=restaurant_ids)).prefetch_related(
                Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date()))
            )

        self.queryset = daily_menus_results.union(restaurants_results).order_by('-rating')

        print('----------------------')
        print(daily_menus_ids)
        print(restaurant_ids)
        print('----------------------')

        return super().get_queryset()


class RegistrationView(APIView):
    authentication_classes = []
    model = get_user_model()
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            send_mail(
                'Vítejte v AťChutná.cz!',
                'Dobrý den!\n' +
                'Vítejte v doporučovacím systému AťChutná.cz!',
                'info@atchutna.cz',
                [user.email],
                fail_silently=True, )

            return Response(UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    authentication_classes = []
    model = get_user_model()
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request):
        email = request.data['email']

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        chars = string.ascii_letters
        random_password = ''.join(random.choice(chars) for i in range(0, 7))

        user.set_password(random_password)
        user.save()

        send_mail(
            'Nové heslo [AťChutná.cz]',
            'Vaše heslo k účtu na AťChutná.cz je ' + random_password,
            'info@atchutna.cz',
            [email],
            fail_silently=False,
        )

        return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)


############################################################################


class FavouriteRestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Restaurant.objects.order_by('-rating', 'name')
    serializer_class = RestaurantWithMenuSerializer

    def get_queryset(self):
        return self.queryset.prefetch_related(
            Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date())),

        ).annotate(
            like_count=Count(
                'daily_menu__dailymenurating',
                filter=(
                        Q(daily_menu__dailymenurating__user=self.request.user) &
                        Q(daily_menu__dailymenurating__liked=True) &
                        # Q(daily_menu__dailymenurating__had=True) &
                        Q(daily_menu__dailymenurating__created_at__gte=timezone.now().date() - timedelta(days=15))
                ),
            )
        ).filter(
            like_count__gte=3
        )


class RecommendedDailyMenusViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RecommenderSerializer
    queryset = Recommender.objects.order_by('order')
    pagination_class = None

    def get_queryset(self):
        if 'type' in self.request.query_params and self.request.query_params['type'] == 'friends':
            self.queryset = self.queryset.filter(with_friends=True)

        return self.queryset.prefetch_related(
            Prefetch('recommendation_set', queryset=Recommendation.objects.filter(
                day=timezone.now().date(),
                user=self.request.user
            )),
            'recommendation_set__friendsrecommendation_set',
            'recommendation_set__friendsrecommendation_set__friend',
            'recommendation_set__menu',
            'recommendation_set__menu__dailymenurating_set',
            'recommendation_set__menu__restaurant'
        ).filter(
            recommendation__user=self.request.user,
            recommendation__day=timezone.now().date(),
        ).distinct()

    def post(self, request, *args, **kwargs):

        generators = Recommender.objects.order_by('order')

        if 'type' in self.request.query_params and self.request.query_params['type'] == 'friends':
            self.queryset = self.queryset.filter(with_friends=True)
            generators.filter(with_friends=True)

        saver = RecommendationSaver()
        generators = generators.all()

        for generator in generators:
            saver.save_recommendations(generator, request.user)

        return self.list(request, args, kwargs)


class DailyMenuRatingViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DailyMenuRatingSerializer

    queryset = DailyMenuRating.objects

    def get_queryset(self):
        return DailyMenuRating.objects.prefetch_related('daily_menu').filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data

        daily_menu = DailyMenu.objects.filter(pk=data['daily_menu']).first()

        if daily_menu is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        points = 1 if data['liked'] else -1

        daily_menu.restaurant.rating += points
        daily_menu.restaurant.save()

        return super().create(request, *args, **kwargs)


class WatchedRestaurantsViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = RestaurantWithMenuSerializer
    queryset = Restaurant.objects
    model = Restaurant

    def list(self, request, *args, **kwargs):
        self.queryset = request.user.watched_restaurants.prefetch_related(
            Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date()))
        ).annotate(
            watched=Value(True, output_field=BooleanField())
        ).order_by('-rating', 'name').all()

        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = request.user
        restaurant = Restaurant.objects.filter(pk=pk).prefetch_related(
            Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date()))
        ).annotate(watched=Value(True, output_field=BooleanField())).first()

        user.watched_restaurants.remove(restaurant)
        response = status.HTTP_200_OK

        return Response(self.serializer_class(restaurant).data, status=response)

    def create(self, request: Request, *args, **kwargs):
        data = request.data
        user = request.user

        restaurant = Restaurant.objects.filter(pk=data['restaurant_id']).prefetch_related(
            Prefetch('daily_menu', queryset=DailyMenu.objects.filter(day=timezone.now().date()))
        ).annotate(watched=Value(True, output_field=BooleanField())).first()

        user.watched_restaurants.add(restaurant)
        response = status.HTTP_201_CREATED

        return Response(self.serializer_class(restaurant).data, status=response)


class MeViewSet(viewsets.ModelViewSet):
    """
    Get information about currently logged user
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self) -> Any:
        return self.request.user

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = self.get_object()

        if 'first_name' in request.data:
            user.first_name = request.data['first_name']

        if 'last_name' in request.data:
            user.last_name = request.data['last_name']

        if 'password' in request.data:
            user.set_password(request.data['password'])

        user.save()

        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)

    def list(self, request: Request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PreferencesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserManualClassification.objects
    serializer_class = PreferencesSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        classification = request.user.manual_classification

        if classification is None:
            classification = UserManualClassification()
            classification.save()

            request.user.manual_classification = classification
            request.user.save()

        return Response(self.serializer_class(classification).data)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        classification = request.user.manual_classification

        if classification is None:
            classification = UserManualClassification(user=request.user)
            classification.save()

            request.user.manual_classification = classification
            request.user.save()

        preference = request.data['item']
        value = request.data['value']

        if preference == 'user_id':
            return Response({}, status=400)

        setattr(classification, preference, value)
        classification.save()

        return Response(self.serializer_class(classification).data, status=status.HTTP_200_OK)


class CousineTaggerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = DailyMenu.objects.filter(cousine_set=False)
    serializer_class = DailyMenuSerializer

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        self.queryset = self.queryset.filter(
            day__gte=timezone.now().date() - timedelta(days=30)
        ).order_by('?')[:5]

        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        meal = self.get_object()

        data = request.data
        if data['cousine'] != 'none':
            cousine = Cousine.objects.filter(classification_column=data['cousine']).first()

            if cousine is None:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            meal.cousine = cousine

        meal.cousine_set = True
        meal.save()

        return Response(self.serializer_class(meal).data, status=status.HTTP_200_OK)


class FriendsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Friendship.objects
    serializer_class = FriendsSerializer
    pagination_class = None

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        try:
            friendship = Friendship(user=self.request.user, friend=user)
            friendship.save()
        except IntegrityError:
            return Response({}, status=status.HTTP_409_CONFLICT)

        return Response(self.serializer_class(friendship).data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        friendship = self.get_object()

        if friendship.user_id != self.request.user.id:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        friendship.delete()

        return Response(self.serializer_class(friendship).data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data

        friendship = self.get_object()
        friendship.lunch_together = data['lunch_together']
        friendship.save()

        return Response(self.serializer_class(friendship).data, status=status.HTTP_200_OK)

    def list(self, request: Request, *args, **kwargs):
        self.queryset = request.user.friends_set.prefetch_related('friend').all()

        return super().list(request, args, kwargs)


class RecommendationLocationViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = UserRecommendationLocation.objects
    serializer_class = RecommendationLocationSerializer
    pagination_class = None

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        query = request.query_params
        type = query['type'] if 'type' in query else 'personal'
        location = self.queryset.filter(type=type).first()

        return Response(self.serializer_class(location).data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data

        location = request.user.locations.filter(type=data['type']).first()

        if location is None:
            location = UserRecommendationLocation(user=request.user)

        location.type = data['type']
        location.recommendation_type = data['recommendation_type']
        location.gps_lat = data['gps_lat']
        location.gps_lng = data['gps_lng']
        location.save(0)

        return Response(self.serializer_class(location).data, status=status.HTTP_200_OK)
