from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from classification.models import NotMealTags
from classification.tagger.not_meals_tagger import NotMealsTagger
from restaurants.models import DailyMenu, Restaurant
from user.models import DailyMenuRating, User


class TestNoMealTagger(TestCase):

    def setUp(self):
        restaurant = Restaurant(name="testing")
        restaurant.save()

        a = DailyMenu(restaurant=restaurant, name="Poledni menu", day=timezone.now().date())
        a.save()

        b = DailyMenu(restaurant=restaurant, name="Poledni nabidka", day=timezone.now().date())
        b.save()

        user = User(first_name="Test", last_name="Test", username="test@example.com")
        user.save()

        DailyMenuRating(daily_menu=a, user=user, is_meal=False).save()
        DailyMenuRating(daily_menu=b, user=user, is_meal=False).save()

    def test_get_tags(self):
        tagger = NotMealsTagger()

        tags = tagger.get_not_meals()

        self.assertIn('poledne', tags)
        self.assertIn('menu', tags)
        self.assertIn('nabidka', tags)

    def test_count_tags(self):
        tagger = NotMealsTagger()

        tags = tagger.get_not_meals()

        self.assertEqual(2, tags['poledne'])
        self.assertEqual(1, tags['menu'])
        self.assertEqual(1, tags['nabidka'])

    def test_save(self):
        tagger = NotMealsTagger()

        tagger.tag(2)

        tags = NotMealTags.objects.all()

        self.assertEqual(1, len(tags))

        self.assertEqual('poledne', tags[0].tag)
