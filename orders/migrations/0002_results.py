# Generated by Django 4.0.1 on 2022-01-24 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_coordinate', models.FloatField()),
                ('first_restaurant', models.FloatField()),
                ('first_duration_restaurant', models.FloatField()),
                ('first_distance_restaurant', models.FloatField()),
                ('firts_route_cost', models.FloatField()),
                ('second_restaurante', models.FloatField()),
                ('second_duration_restaurant', models.FloatField()),
                ('second_distance_restaurant', models.FloatField()),
                ('second_route_cost', models.FloatField()),
                ('third_restaurant', models.FloatField()),
                ('third_duration_restaurant', models.FloatField()),
                ('third_distance_restaurant', models.FloatField()),
                ('third_route_cost', models.FloatField()),
                ('pizza_order_amount', models.FloatField()),
                ('first_restaurant_production_time', models.FloatField()),
                ('second_restaurant_production_time', models.FloatField()),
                ('third_restaurant_production_time', models.FloatField()),
                ('first_restaurant_capacity', models.FloatField()),
                ('second_restaurant_capacity', models.FloatField()),
                ('third_restaurant_capacity', models.FloatField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders')),
            ],
        ),
    ]