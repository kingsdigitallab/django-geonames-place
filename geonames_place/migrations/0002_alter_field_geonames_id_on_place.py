# Generated by Django 2.1.3 on 2018-11-14 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonames_place', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='geonames_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
