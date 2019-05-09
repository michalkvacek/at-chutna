from django.test import TestCase

from crawler.data_cleaners.daily_menu.cleaner import DailyMenuCleaner
from crawler.data_cleaners.ingredients.cleaner import IngredientsCleaner


class TestIngredientsCleaner(TestCase):

    def setUp(self):
        self.cleaner = IngredientsCleaner()

    def test_ingredients(self):

        ingredients = [
            "1dkg hladké mouky (nebo více)",
            "1 dkg hladké mouky     "
        ]

        cleaned = self.cleaner.clean(ingredients)

        for ingredient in cleaned:
            self.assertEqual(ingredient, "hladké mouky")

    def test_empty_ingredients(self):

        ingredients = [
            "(nebo více)",
            "     ",
            "0.5kg",
            "0.5 kg"
        ]

        cleaned = self.cleaner.clean(ingredients)

        self.assertEqual(0, len(cleaned))

