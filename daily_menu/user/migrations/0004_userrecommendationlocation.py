# Generated by Django 2.1.4 on 2019-05-05 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_recommender_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRecommendationLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=64)),
                ('gps_lat', models.FloatField(blank=True, default=None, null=True)),
                ('gps_lng', models.FloatField(blank=True, default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]