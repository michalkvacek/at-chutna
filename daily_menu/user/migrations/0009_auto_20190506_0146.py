# Generated by Django 2.1.4 on 2019-05-05 23:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190506_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendsRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Recommendation')),
            ],
        ),
        migrations.AddField(
            model_name='recommender',
            name='with_friends',
            field=models.BooleanField(default=False),
        ),
    ]
