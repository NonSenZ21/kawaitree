# Generated by Django 4.0.4 on 2022-05-08 09:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_don_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='don_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 5, 8, 9, 34, 29, 879565), null=True, verbose_name='Last donation date'),
        ),
    ]
