# Generated by Django 4.0.4 on 2022-05-07 07:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_fb_profile_insta_profile_yt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='expert',
            field=models.BooleanField(default=False, verbose_name='Disable helpers'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='don_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 7, 7, 56, 14, 991343)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weather',
            field=models.BooleanField(default=False, verbose_name='Weather alerts'),
        ),
    ]