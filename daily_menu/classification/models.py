from django.db import models


class Classification(models.Model):
    class Meta:
        abstract = True

    vegetarian = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    vegan = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    meat = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    beef = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    pork = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    venison = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    fish = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    poultry = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    seafood = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    pasta = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    tofu = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    cheese = models.FloatField(
        default=None,
        blank=True,
        null=True
    )
    mushrooms = models.FloatField(
        default=None,
        blank=True,
        null=True
    )

    indian = models.FloatField(default=None, blank=True, null=True)
    vietnamese = models.FloatField(default=None, blank=True, null=True)
    mexican = models.FloatField(default=None, blank=True, null=True)
    czech = models.FloatField(default=None, blank=True, null=True)
    american = models.FloatField(default=None, blank=True, null=True)
    chinese = models.FloatField(default=None, blank=True, null=True)
    japanese = models.FloatField(default=None, blank=True, null=True)
    italian = models.FloatField(default=None, blank=True, null=True)
    soup = models.FloatField(default=None, blank=True, null=True)
    sweet = models.FloatField(default=None, blank=True, null=True)



class DailyMenuClassification(Classification):
    pass


class UserClassification(Classification):
    pass


class UserManualClassification(Classification):
    """This class contains preferences set manullay via profile edit"""
    pass


class NotMealTags(models.Model):
    """
    Tags extracted from NotMeals table
    """
    tag = models.TextField()
    frequency = models.FloatField(
        null=True,
        blank=True,
    )
    is_significant = models.BooleanField(
        default=False
    )


class TagGeneralization(models.Model):
    tag = models.TextField(max_length=250)
    extra_tag = models.TextField(max_length=250)
    tag_canonical = models.TextField(max_length=250, blank=True, null=True)
    extra_tag_canonical = models.TextField(max_length=250, blank=True, null=True)
