# Generated by Django 4.0.2 on 2022-04-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_photo_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to='trees-tasks_pics', verbose_name='Thumbnail'),
        ),
    ]