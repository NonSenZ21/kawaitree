# Generated by Django 4.0.4 on 2022-05-09 17:30

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_profile_don_date_alter_profile_max_wind'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wnday', models.IntegerField(default=0, verbose_name='Day number')),
                ('wdate', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('wid', models.IntegerField(default=0, verbose_name='Weather code')),
                ('wmain', models.CharField(max_length=100, verbose_name='Weather main')),
                ('wdescription', models.CharField(max_length=150, verbose_name='Weather description')),
                ('wtemp_min', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Min temperature')),
                ('wtemp_max', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Max temperature')),
                ('wwind_gust', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Gusts speed')),
                ('wicon', models.CharField(max_length=10, verbose_name='Weather icon')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='don_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 5, 9, 17, 30, 53, 663338), null=True, verbose_name='Last donation date'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='expert',
            field=models.BooleanField(default=False, verbose_name='Expert (disable helpers)'),
        ),
    ]