# Generated by Django 4.0.2 on 2022-04-03 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_tree_adate_alter_tree_bdate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oname', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='tree',
            name='shop',
        ),
        migrations.AlterField(
            model_name='tree',
            name='speciesfk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.species', verbose_name='Species'),
        ),
        migrations.AddField(
            model_name='tree',
            name='originfk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.origin', verbose_name='Origin'),
        ),
    ]