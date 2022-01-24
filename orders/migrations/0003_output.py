# Generated by Django 4.0.1 on 2022-01-24 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_coordinate', models.FloatField(blank=True, null=True)),
                ('first_restaurant', models.FloatField(blank=True, null=True)),
                ('route_cost', models.FloatField(blank=True, null=True)),
                ('second_restaurante', models.FloatField(blank=True, null=True)),
                ('third_restaurant', models.FloatField(blank=True, null=True)),
                ('pizza_order_amount', models.FloatField(blank=True, null=True)),
                ('production_time', models.FloatField(blank=True, null=True)),
                ('capacity', models.FloatField(blank=True, null=True)),
                ('vehicle_type', models.FloatField(blank=True, null=True)),
                ('vehicle_cost', models.FloatField(blank=True, null=True)),
                ('total_cost_restaurant', models.FloatField(blank=True, null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders')),
            ],
        ),
    ]