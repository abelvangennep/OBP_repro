# Generated by Django 4.0.1 on 2022-01-26 19:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurants',
            name='restaurant_id_pizza',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='busy_until',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 26, 0, 0, 1, 193068), null=True),
        ),
    ]