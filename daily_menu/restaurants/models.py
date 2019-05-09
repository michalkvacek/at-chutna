from django.db import models

from classification.models import DailyMenuClassification


class Cousine(models.Model):
    name = models.CharField(
        max_length=250
    )
    classification_column = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Name of the restaurant',
    )
    menu_url = models.URLField(
        max_length=2048,
        blank=True,
        null=True,
    )

    address = models.CharField(
        max_length=256,
        help_text='Restaurant address',
        default=None,
        blank=True,
        null=True
    )

    rating = models.IntegerField(
        default=0,
        help_text="Automatically computed rating, based on menu rating"
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

    cousine = models.ForeignKey(
        Cousine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        """
        Print model - use restaurant's name
        :return:  string restaurant's name
        """
        return self.name


class DailyMenu(models.Model):
    name = models.CharField(
        max_length=256,
        help_text="Meal name",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    day = models.DateField()

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="daily_menu"
    )

    automatic_classification = models.ForeignKey(
        DailyMenuClassification,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True
    )

    classification_in_progress = models.BooleanField(
        default=False
    )

    cousine = models.ForeignKey(
        Cousine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    cousine_set = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class DailyMenuTags(models.Model):
    daily_menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    tag = models.CharField(
        max_length=250
    )


class CousineTags(models.Model):
    cousine = models.ForeignKey(Cousine, on_delete=models.CASCADE)
    tag = models.TextField(max_length=250)
