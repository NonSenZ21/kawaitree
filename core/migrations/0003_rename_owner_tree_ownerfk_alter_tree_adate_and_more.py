# Generated by Django 4.0.2 on 2022-03-06 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_name_tree_tname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tree',
            old_name='owner',
            new_name='ownerfk',
        ),
        migrations.AlterField(
            model_name='tree',
            name='adate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tree',
            name='bdate',
            field=models.DateField(null=True),
        ),
    ]
