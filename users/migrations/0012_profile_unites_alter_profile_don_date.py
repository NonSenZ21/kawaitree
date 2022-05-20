# Generated by Django 4.0.4 on 2022-05-08 17:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_profile_don_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='unites',
            field=models.CharField(default='1', max_length=1, verbose_name='Units'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='don_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 5, 8, 17, 22, 4, 981115), null=True, verbose_name='Last donation date'),
        ),
    ]