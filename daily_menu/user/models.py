from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from classification.models import UserClassification, UserManualClassification
from restaurants.models import Restaurant, DailyMenu


class User(AbstractUser):
    watched_restaurants = models.ManyToManyField(Restaurant)

    automatic_classification = models.ForeignKey(
        UserClassification,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True

    )
    manual_classification = models.ForeignKey(
        UserManualClassification,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True
    )


class Friendship(models.Model):
    lunch_together = models.BooleanField(default=True)
    user = models.ForeignKey(
        get_user_model(),
        related_name="friends_set",
        on_delete=models.CASCADE
    )

    friend = models.ForeignKey(
        get_user_model(),
        related_name="friendship_creator_set",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('friend', 'user',)


class Recommender(models.Model):
    name = models.CharField(
        max_length=250,
    )

    description = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        default=None,
    )

    recommendation_class = models.CharField(
        max_length=250
    )

    with_friends = models.BooleanField(
        default=False
    )

    order = models.IntegerField()


class Recommendation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    recommender = models.ForeignKey(
        Recommender,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    day = models.DateField(auto_now_add=True)


class FriendsRecommendation(models.Model):
    recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.CASCADE,
    )

    friend = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )


class DailyMenuRating(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    daily_menu = models.ForeignKey(
        DailyMenu,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True
    )

    liked = models.BooleanField(
        blank=True,
        null=True
    )

    had = models.BooleanField(
        blank=True,
        null=True
    )

    is_meal = models.BooleanField(
        blank=True,
        null=True,
        default=None
    )


class UserRecommendationLocation(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="locations"
    )
    type = models.CharField(
        max_length=64,
        help_text="Use for recommending for friends or only for user?"
    )

    recommendation_type = models.CharField(
        max_length=64,
        default='restaurants',
        help_text="Use position or visited restaurants?"
    )

    gps_lat = models.FloatField(
        default=None,
        blank=True,
        null=True
    )

    gps_lng = models.FloatField(
        default=None,
        blank=True,
        null=True
    )

# class Common
