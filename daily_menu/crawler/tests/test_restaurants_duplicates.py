from django.test import TestCase

from crawler.data_cleaners.daily_menu.cleaner import DailyMenuCleaner
from crawler.data_cleaners.ingredients.cleaner import IngredientsCleaner
from crawler.scrapers.restaurant_duplicates_checker import RestaurantDuplicatesChecker
from restaurants.models import Restaurant


class TestRestaurantsDuplicates(TestCase):

    def setUp(self):
        Restaurant(
            name="testovaci restaurace",
            gps_lat=50.0,
            gps_lng=14.0
        ).save()

        Restaurant(
            name="druha restaurace",

        ).save()

        self.checker = RestaurantDuplicatesChecker()

    def test_same_name_no_gps(self):
        result = self.checker.already_exists("testovaci restaurace", (None, None))

        self.assertTrue(result)

    def test_same_name_with_gps(self):
        result = self.checker.already_exists("testovaci restaurace", (50.0005, 13.9995))

        self.assertTrue(result)

    def test_same_name_different_location(self):
        result = self.checker.already_exists("testovaci restaurace", (51.0005, 13.9995))

        self.assertFalse(result)

    def test_no_gps(self):
        result = self.checker.already_exists("druha restaurace", (None, None))

        self.assertTrue(result)

    def test_non_existing_restaurant(self):
        result = self.checker.already_exists("Uplne nova restaurace", (None, None))

        self.assertFalse(result)
