# Generated by Django 2.1.4 on 2019-05-08 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailymenuclassification',
            name='potatoes',
        ),
        migrations.RemoveField(
            model_name='dailymenuclassification',
            name='rice',
        ),
        migrations.RemoveField(
            model_name='userclassification',
            name='potatoes',
        ),
        migrations.RemoveField(
            model_name='userclassification',
            name='rice',
        ),
        migrations.RemoveField(
            model_name='usermanualclassification',
            name='potatoes',
        ),
        migrations.RemoveField(
            model_name='usermanualclassification',
            name='rice',
        ),
        migrations.AddField(
            model_name='dailymenuclassification',
            name='japanese',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='dailymenuclassification',
            name='soup',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='dailymenuclassification',
            name='sweet',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='userclassification',
            name='japanese',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='userclassification',
            name='soup',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='userclassification',
            name='sweet',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='usermanualclassification',
            name='japanese',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='usermanualclassification',
            name='soup',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='usermanualclassification',
            name='sweet',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
