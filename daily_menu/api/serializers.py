import hashlib
from django.contrib.auth import get_user_model
from rest_framework import serializers

from classification.models import UserManualClassification
from restaurants.models import Restaurant, DailyMenu
from user.models import Recommendation, DailyMenuRating, Recommender, UserRecommendationLocation, Friendship


class DailyMenuRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DailyMenuRating
        fields = ('id', 'had', 'liked', 'is_meal', 'daily_menu', 'user')


class DailyMenuSerializer(serializers.ModelSerializer):
    rating = DailyMenuRatingSerializer(source='dailymenurating_set', many=True)

    class Meta:
        model = DailyMenu
        fields = ('id', 'name', 'price', 'day', 'rating',)
        read_only_fields = ('id',)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_url', 'address', 'gps_lat', 'gps_lng')
        read_only_fields = ('id',)


class RestaurantWithMenuSerializer(serializers.ModelSerializer):
    daily_menu = DailyMenuSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_url', 'rating', 'daily_menu', 'address', 'gps_lat', 'gps_lng')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    @staticmethod
    def get_avatar(instance):
        avatar = hashlib.md5(instance.email.lower().encode('utf-8')).hexdigest()

        return "https://s.gravatar.com/avatar/" + avatar

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'avatar', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class FriendsSerializer(serializers.ModelSerializer):
    friend = UserSerializer()

    class Meta:
        model = Friendship
        fields = ('id', 'lunch_together', 'friend',)



class RecommendationSerializer(serializers.ModelSerializer):
    daily_menu = DailyMenuSerializer(source="menu")
    friends = serializers.SerializerMethodField()
    restaurant = RestaurantSerializer(source="menu.restaurant")

    @staticmethod
    def get_friends(instance):
        users = []
        for recommendation in instance.friendsrecommendation_set.all():
            users.append(recommendation.friend)


        return UserSerializer(users, many=True).data

    class Meta:
        model = Recommendation
        fields = ('friends', 'restaurant', 'daily_menu', 'restaurant', 'day',)


class RecommenderSerializer(serializers.ModelSerializer):
    recommendations = RecommendationSerializer(source="recommendation_set", many=True)

    class Meta:
        model = Recommender
        fields = ('name', 'description', 'id', 'recommendations')


class RecommendationLocationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserRecommendationLocation
        fields = ('user', 'gps_lat', 'gps_lng', 'type', 'recommendation_type',)


class PreferencesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserManualClassification
        fields = (
            'user',
            'vegetarian',
            'vegan',
            'meat',
            'beef',
            'pork',
            'venison',
            'fish',
            'poultry',
            'seafood',
            'pasta',
            'tofu',
            'sweet',
            'soup',
            'japanese',
            'cheese',
            'mushrooms',
            'indian',
            'vietnamese',
            'mexican',
            'czech',
            'american',
            'chinese',
            'italian',
        )
