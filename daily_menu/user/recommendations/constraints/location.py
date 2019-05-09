from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from user.models import DailyMenuRating
from user.recommendations.constraints.base_constraint import BaseConstraint


class LocationConstraint(BaseConstraint):

    def __init__(self, user, classification, location):
        super().__init__(user, classification)

        self.location = location

    def _get_visited_restaurants(self):
        ratings = DailyMenuRating.objects.filter(
            had=True,
            liked=True,
            daily_menu__day__gte=timezone.now().date() - timedelta(days=30)
        ).prefetch_related('daily_menu', 'daily_menu__restaurant')

        # Restaurants
        restaurants = [rating.daily_menu.restaurant for rating in ratings]

        return restaurants

    def _filter_by_visited_restaurants(self, query):
        restaurants = self._get_visited_restaurants()

        radius = 0.002
        final_filter = Q()
        for restaurant in restaurants:

            if restaurant.gps_lat is not None and restaurant.gps_lng is not None:
                final_filter.add(
                    self._get_location_filter(restaurant.gps_lat, restaurant.gps_lng, radius),
                    Q.OR
                )

        return query.filter(final_filter)

    def _get_location_filter(self, lat, lng, radius):
        return (
                Q(restaurant__gps_lat__gte=lat - radius) &
                Q(restaurant__gps_lat__lte=lat + radius) &
                Q(restaurant__gps_lng__gte=lng - radius) &
                Q(restaurant__gps_lng__lte=lng + radius)
        )

    def filter(self, query):
        query = query.exclude(restaurant__pk=3922)

        if self.location.recommendation_type == 'restaurants':
            return self._filter_by_visited_restaurants(query)
        else:
            return query.filter(self._get_location_filter(self.location.gps_lat, self.location.gps_lng, 0.01)) # +- 2km diameter
