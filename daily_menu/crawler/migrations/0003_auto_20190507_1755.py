# Generated by Django 2.1.4 on 2019-05-07 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20190507_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantscraperconfig',
            old_name='menu_parser',
            new_name='menu_scraper',
        ),
        migrations.RenameField(
            model_name='restaurantscraperconfig',
            old_name='parser_parameters',
            new_name='scraper_parameters',
        ),
    ]
