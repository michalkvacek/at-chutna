from django.test import TestCase
from django.utils import timezone

from classification.classificators.daily_menu_classificator import DailyMenuClassificator
from classification.models import DailyMenuClassification
from restaurants.models import Restaurant, DailyMenu
from user.models import User
from user.recommendations.loaders.base import UserMenuLoader


# Create your tests here.


class TestRecommendationsLoader(TestCase):

    def setUp(self):
        self.user = User(first_name="Test", last_name="Test", username="test-location@example.com")
        self.user.save()

        classification_columns = DailyMenuClassificator().get_classification_columns()
        self.classification = {}
        for column in classification_columns:
            self.classification[column] = 0

        restaurant = Restaurant(name="recommendation_loader_test")
        restaurant.save()

        c1 = DailyMenuClassification(meat=1, vegetarian=0, fish=0)
        c1.save()
        c2 = DailyMenuClassification(meat=0, vegetarian=1, fish=0)
        c2.save()

        DailyMenu.objects.all().delete()

        a = DailyMenu(day=timezone.now().date(), restaurant=restaurant, name="maso", automatic_classification=c1)
        a.save()

        b = DailyMenu(day=timezone.now().date(), restaurant=restaurant, name="vegetarian", automatic_classification=c2)
        b.save()

    def test_filter_by_classification(self):
        classification = self.classification

        classification['vegetarian'] = -0.7

        loader = UserMenuLoader(self.user, classification)

        menus = DailyMenu.objects.prefetch_related('automatic_classification').all()
        menus = loader.filter_by_classification(menus)

        self.assertEqual(1, len(menus))
        self.assertEqual('maso', menus[0].name)

    def test_filter_by_low_classification(self):
        c1 = DailyMenuClassification()

        for column in self.classification:
            setattr(c1, column, 0.7)

        c1.save()

        restaurant = Restaurant(name='test')
        restaurant.save()

        a = DailyMenu(day=timezone.now().date(), restaurant=restaurant, name="random", automatic_classification=c1)
        a.save()

        menus = DailyMenu.objects.prefetch_related('automatic_classification').all()

        loader = UserMenuLoader(self.user, self.classification)

        self.assertEqual(3, len(menus))

        menus = loader.filter_menus_with_low_classification(menus)

        self.assertEqual(1, len(menus))
        self.assertEqual('random', menus[0].name)
