# Generated by Django 4.0.1 on 2022-01-28 11:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_restaurants_busy_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurants',
            name='busy_until',
            field=models.TimeField(blank=True, default=datetime.datetime(2022, 1, 28, 0, 0, 1, 591815), null=True),
        ),
        migrations.CreateModel(
            name='Deliverers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity_available', models.PositiveBigIntegerField()),
                ('orders', models.ManyToManyField(to='orders.Orders')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.vehicles')),
            ],
        ),
    ]
