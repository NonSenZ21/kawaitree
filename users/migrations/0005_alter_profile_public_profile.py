# Generated by Django 4.0.6 on 2022-07-23 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_weather_wdate0_remove_weather_wdate1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='public_profile',
            field=models.BooleanField(default=True, verbose_name='Public profile'),
        ),
    ]
