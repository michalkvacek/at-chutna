from django.test import TestCase

# Create your tests here.
from django.utils import timezone

from restaurants.models import Restaurant, DailyMenu
from user.models import User, UserRecommendationLocation, DailyMenuRating
from user.recommendations.constraints.location import LocationConstraint


class TestRestaurantsLocationFilter(TestCase):

    def setUp(self):
        # radius 0.002

        restaurants = [
            Restaurant(name="A", gps_lat=50.0019, gps_lng=14.001),
            Restaurant(name="B", gps_lat=50.05, gps_lng=13.9),
            Restaurant(name="C", gps_lat=49.999, gps_lng=14),
            Restaurant(name="D", gps_lat=51, gps_lng=14),
            Restaurant(name="D", gps_lat=51.005, gps_lng=14),
            Restaurant(name="E", gps_lat=50, gps_lng=14.002),
            Restaurant(name="F", gps_lat=50.002, gps_lng=14.002),
            Restaurant(name="G", gps_lat=49.998, gps_lng=13.998),
        ]

        for restaurant in restaurants:
            restaurant.save()
            menu = DailyMenu(restaurant=restaurant, name="Testing - nearby", day=timezone.now().date())
            menu.save()

        restaurant = Restaurant(name="Moje", gps_lat=50, gps_lng=14)
        restaurant.save()
        menu = DailyMenu(restaurant=restaurant, name="Testing", day=timezone.now().date())
        menu.save()

        user = User(first_name="Test", last_name="Test", username="test-location@example.com")
        user.save()

        self.user = user

        DailyMenuRating(daily_menu=menu, user=user, is_meal=True, had=True, liked=True).save()

    def test_restaurants_nearby(self):
        query = DailyMenu.objects

        location = UserRecommendationLocation(user=self.user, type="personal", recommendation_type="restaurants")
        location.save()

        filter = LocationConstraint(self.user, None, location)
        query = filter.filter(query)
        restaurants = query.all()

        self.assertEqual(6, len(restaurants))

    def test_position(self):
        query = DailyMenu.objects

        location = UserRecommendationLocation(user=self.user, type="personal", recommendation_type="position",
                                              gps_lat=51.001, gps_lng=14)
        location.save()

        filter = LocationConstraint(self.user, None, location)
        query = filter.filter(query)
        restaurants = query.all()

        self.assertEqual(2, len(restaurants))
