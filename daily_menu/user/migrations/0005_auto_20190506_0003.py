# Generated by Django 2.1.4 on 2019-05-05 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_userrecommendationlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecommendationlocation',
            name='type',
            field=models.CharField(help_text='Use for recommending for friends or only for user?', max_length=64),
        ),
        migrations.AlterField(
            model_name='userrecommendationlocation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to=settings.AUTH_USER_MODEL),
        ),
    ]
