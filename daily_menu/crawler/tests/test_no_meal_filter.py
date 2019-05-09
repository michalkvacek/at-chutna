from django.test import TestCase
from django.utils import timezone

from classification.tagger.not_meals_tagger import NotMealsTagger
from crawler.data_cleaners.daily_menu.cleaner import DailyMenuCleaner
from restaurants.models import Restaurant, DailyMenu
from user.models import User, DailyMenuRating


class TestNoMealFilter(TestCase):
    def setUp(self):
        restaurant = Restaurant(name="testing")
        restaurant.save()

        a = DailyMenu(restaurant=restaurant, name="Poledni menu", day=timezone.now().date())
        a.save()

        b = DailyMenu(restaurant=restaurant, name="Poledni nabidka", day=timezone.now().date())
        b.save()

        c = DailyMenu(restaurant=restaurant, name="Poledni menu", day=timezone.now().date())
        c.save()

        d = DailyMenu(restaurant=restaurant, name="Hlavni jidlo", day=timezone.now().date())
        d.save()

        e = DailyMenu(restaurant=restaurant, name="Hlavni chod", day=timezone.now().date())
        e.save()

        user = User(first_name="Test", last_name="Test", username="test-no-meal@example.com")
        user.save()

        DailyMenuRating(daily_menu=a, user=user, is_meal=False).save()
        DailyMenuRating(daily_menu=b, user=user, is_meal=False).save()
        DailyMenuRating(daily_menu=c, user=user, is_meal=False).save()
        DailyMenuRating(daily_menu=d, user=user, is_meal=False).save()
        DailyMenuRating(daily_menu=e, user=user, is_meal=False).save()


        tagger = NotMealsTagger()
        tagger.tag(2)

    def test_neco(self):
        menus = [
            {'name': 'Hlavní chod dne', 'price': ''},
            {'name': 'Polední chod', 'price': ''},
            {'name': 'Hlavní chod: krupicova kase', 'price': ''},
        ]

        cleaner = DailyMenuCleaner()
        cleaned = cleaner.clean_daily_menu(menus)

        self.assertEqual(1, len(cleaned))




