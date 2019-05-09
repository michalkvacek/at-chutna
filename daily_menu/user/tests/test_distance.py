from django.test import TestCase
from django.utils import timezone

from classification.classificators.daily_menu_classificator import DailyMenuClassificator
from classification.models import DailyMenuClassification
from restaurants.models import Restaurant, DailyMenu
from user.models import User
from user.recommendations.loaders.base import UserMenuLoader


# Create your tests here.
from user.recommendations.similarity import VectorDistance


class TestDistance(TestCase):
    # def setUp(self):
    #     self.user = User(first_name="Test", last_name="Test", username="test-location@example.com")
    #     self.user.save()
    #
    #     classification_columns = DailyMenuClassificator().get_classification_columns()
    #     self.classification = {}
    #     for column in classification_columns:
    #         self.classification[column] = 0
    #
    #     restaurant = Restaurant(name="recommendation_loader_test")
    #     restaurant.save()
    #
    #     c1 = DailyMenuClassification(meat=1, vegetarian=0, fish=0)
    #     c1.save()
    #     c2 = DailyMenuClassification(meat=0, vegetarian=1, fish=0)
    #     c2.save()
    #
    #     DailyMenu.objects.all().delete()
    #
    #     a = DailyMenu(day=timezone.now().date(), restaurant=restaurant, name="maso", automatic_classification=c1)
    #     a.save()
    #
    #     b = DailyMenu(day=timezone.now().date(), restaurant=restaurant, name="vegetarian", automatic_classification=c2)
    #     b.save()

    def test_full_classification_identity(self):
        classification_columns = DailyMenuClassificator().get_classification_columns()

        classification = {}
        for column in classification_columns:
            classification[column] = 0

        menu_classification = DailyMenuClassification()
        for column in classification_columns:
            setattr(menu_classification, column, 0)
        menu_classification.save()

        distance = VectorDistance()

        self.assertEqual(0, distance.calculate(classification, menu_classification))

    def test_full_classification_opposite(self):
        classification_columns = DailyMenuClassificator().get_classification_columns()[:3]

        classification = {}
        for column in classification_columns:
            classification[column] = -1

        menu_classification = DailyMenuClassification()
        for column in classification_columns:
            setattr(menu_classification, column, 1)
        menu_classification.save()

        distance = VectorDistance()

        self.assertEqual(6, distance.calculate(classification, menu_classification))


    def test_full_classification(self):
        classification_columns = DailyMenuClassificator().get_classification_columns()[:3]

        classification = {}
        for column in classification_columns:
            classification[column] = -1

        classification[classification_columns[0]] = 1

        menu_classification = DailyMenuClassification()
        for column in classification_columns:
            setattr(menu_classification, column, 1)
        menu_classification.save()

        distance = VectorDistance()

        self.assertEqual(4, distance.calculate(classification, menu_classification))



    def test_partial_classification(self):
        classification = {
            'vegan': 1,
            'tofu': 0.5
        }

        menu_classification = DailyMenuClassification()
        menu_classification.vegan = 1
        menu_classification.cheese = 0
        menu_classification.save()

        distance = VectorDistance()

        self.assertEqual(0, distance.calculate(classification, menu_classification))

    def test_partial_classification_2(self):
        classification = {
            'vegan': 1,
            'tofu': 0.5
        }

        menu_classification = DailyMenuClassification()
        menu_classification.vegan = 1
        menu_classification.cheese = 0
        menu_classification.tofu=1
        menu_classification.save()

        distance = VectorDistance()

        self.assertEqual(0.5, distance.calculate(classification, menu_classification))

