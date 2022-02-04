from pickle import TRUE
from django.db import models
from datetime import datetime
from django.db.models import Q

# Create your models here.
class Restaurants(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    pizza_parallel = models.PositiveIntegerField(default=0)
    pizza_production_minutes = models.PositiveIntegerField(default=0)
    shoarma_parallel = models.PositiveIntegerField(default=0)
    shoarma_production_minutes = models.PositiveIntegerField(default=0)
    burger_parallel = models.PositiveIntegerField(default=0)
    burger_production_minutes = models.PositiveIntegerField(default=0)
    fries_parallel = models.PositiveIntegerField(default=0)
    fries_production_minutes = models.PositiveIntegerField(default=0)
    snack_parallel = models.PositiveIntegerField(default=0)
    snack_production_minutes = models.PositiveIntegerField(default=0)
    french_parallel = models.PositiveIntegerField(default=0)
    french_production_minutes = models.PositiveIntegerField(default=0)
    spanish_parallel = models.PositiveIntegerField(default=0)
    spanish_production_minutes = models.PositiveIntegerField(default=0)
    italian_parallel = models.PositiveIntegerField(default=0)
    italian_production_minutes = models.PositiveIntegerField(default=0)
    greek_parallel = models.PositiveIntegerField(default=0)
    greek_production_minutes = models.PositiveIntegerField(default=0)
    german_parallel = models.PositiveIntegerField(default=0)
    german_production_minutes = models.PositiveIntegerField(default=0)
    african_parallel = models.PositiveIntegerField(default=0)
    african_production_minutes = models.PositiveIntegerField(default=0)
    mexican_parallel = models.PositiveIntegerField(default=0)
    mexican_production_minutes = models.PositiveIntegerField(default=0)
    argentine_parallel = models.PositiveIntegerField(default=0)
    argentine_production_minutes = models.PositiveIntegerField(default=0)
    indian_parallel = models.PositiveIntegerField(default=0)
    indian_production_minutes = models.PositiveIntegerField(default=0)
    chinese_parallel = models.PositiveIntegerField(default=0)
    chinese_production_minutes = models.PositiveIntegerField(default=0)
    sushi_parallel = models.PositiveIntegerField(default=0)
    sushi_production_minutes = models.PositiveIntegerField(default=0)
    luxe_parallel = models.PositiveIntegerField(default=0)
    luxe_production_minutes = models.PositiveIntegerField(default=0)
    mon_open = models.TimeField(default=None)
    mon_close = models.TimeField(default=None)
    tue_open = models.TimeField(default=None)
    tue_close = models.TimeField(default=None)
    wed_open = models.TimeField(default=None)
    wed_close = models.TimeField(default=None)
    thu_open = models.TimeField(default=None)
    thu_close = models.TimeField(default=None)
    fri_open = models.TimeField(default=None)
    fri_close = models.TimeField(default=None)
    sat_open = models.TimeField(default=None)
    sat_close = models.TimeField(default=None)
    sun_open = models.TimeField(default=None)
    sun_close = models.TimeField(default=None)
    busy_until = models.TimeField(default=datetime.now().replace(hour=0, minute=0, second=1),null=True, blank=True)
    restaurant_id_pizza = models.PositiveIntegerField(null=True,blank=True)

    @staticmethod
    def fill_id_pizza():
        """Fill the id pizza field, so that the app can filter on pizza only orders"""

        all_restaurants_pizza = Restaurants.objects.filter(~Q(pizza_parallel=0))
        i=0
        for restaurant in all_restaurants_pizza:
            if restaurant.restaurant_id_pizza:
                continue
            else:
                restaurant.restaurant_id_pizza = i
                i = i+1
                restaurant.save(update_fields=['restaurant_id_pizza'])
        return all_restaurants_pizza

class Vehicles(models.Model):
    capacity = models.PositiveIntegerField(default=0)
    fixed_cost = models.PositiveIntegerField(default=0)
    hour_costs = models.PositiveIntegerField(default=0)
    km_costs = models.FloatField(default=0)
    allowed_on_highspeed_roads = models.BinaryField(default=0)

class Orders(models.Model):
    STATES = (
        ('N', 'None'),
        ('R', 'Restaurants'),
        ('D', 'Deliverer'),
    )

    lat = models.FloatField()
    lon = models.FloatField()
    order_time = models.TimeField()
    pizza_amount = models.PositiveIntegerField()
    shoarma_amount = models.PositiveIntegerField()
    burger_amount = models.PositiveIntegerField()
    fries_amount = models.PositiveIntegerField()
    snack_amount = models.PositiveIntegerField()
    french_amount = models.PositiveIntegerField()
    spanish_amount = models.PositiveIntegerField()
    italian_amount = models.PositiveIntegerField()
    greek_amount = models.PositiveIntegerField()
    german_amount = models.PositiveIntegerField()
    african_amount = models.PositiveIntegerField()
    mexican_amount = models.PositiveIntegerField()
    argentine_amount = models.PositiveIntegerField()
    indian_amount = models.PositiveIntegerField()
    chinese_amount = models.PositiveIntegerField()
    sushi_amount = models.PositiveIntegerField()
    luxe_amount = models.PositiveIntegerField()
    state = models.CharField(max_length = 1, choices = STATES, null=True)
    selected_restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE, null=True)
    selected_deliverer = models.ForeignKey(Vehicles, on_delete=models.CASCADE, null=True)

    def _str_(self):
        return f"{self.id}"


class Results(models.Model):
    order_extrabla = models.PositiveIntegerField(null = True, blank =True)
    order_id = models.PositiveIntegerField(null=True, blank=TRUE)
    customer_coordinate = models.FloatField(null=True, blank = True)
    order_time = models.TimeField(null=True, blank =True)
    first_restaurant = models.FloatField(null=True, blank = True)
    first_duration_restaurant = models.FloatField(null=True, blank = True)
    first_distance_restaurant = models.FloatField(null=True, blank = True)
    first_route_cost = models.FloatField(null=True, blank = True)
    second_restaurant = models.FloatField(null=True, blank = True)
    second_duration_restaurant = models.FloatField(null=True, blank = True)
    second_distance_restaurant = models.FloatField(null=True, blank = True)
    second_route_cost = models.FloatField(null=True, blank = True)
    third_restaurant = models.FloatField(null=True, blank = True)
    third_duration_restaurant = models.FloatField(null=True, blank = True)
    third_distance_restaurant = models.FloatField(null=True, blank = True)
    third_route_cost = models.FloatField(null=True, blank = True)
    pizza_order_amount = models.FloatField(null=True, blank = True)
    first_restaurant_capacity = models.FloatField(null=True, blank = True)
    second_restaurant_capacity = models.FloatField(null=True, blank = True)
    third_restaurant_capacity = models.FloatField(null=True, blank = True)
    first_restaurant_production_time = models.FloatField(null=True, blank = True)
    second_restaurant_production_time = models.FloatField(null=True, blank = True)
    third_restaurant_production_time = models.FloatField(null=True, blank = True)
    first_actual_production_time = models.FloatField(null=True, blank=True)
    second_actual_production_time = models.FloatField(null=True, blank=True)
    third_actual_production_time = models.FloatField(null=True, blank=True)
    first_vehicle_type = models.FloatField(null=True, blank = True)
    second_vehicle_type = models.FloatField(null=True, blank = True)
    third_vehicle_type = models.FloatField(null=True, blank = True)
    first_min_vehicle_cost = models.FloatField(null=True, blank=True)
    second_min_vehicle_cost = models.FloatField(null=True, blank = True)
    third_min_vehicle_cost = models.FloatField(null=True, blank = True)
    first_total_cost_restaurant = models.FloatField(null=True, blank = True)
    second_total_cost_restaurant = models.FloatField(null=True, blank = True)
    third_total_cost_restaurant = models.FloatField(null=True, blank = True)
    back_vehicle_cost = models.FloatField(null=True, blank=True)

class Analyses(models.Model):
    order = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)
    customer_coordinate = models.FloatField(null=True, blank = True)
    restaurant_id = models.PositiveIntegerField()
    deliverer_id = models.PositiveIntegerField(default=None, null=True, blank = True)
    route_cost = models.FloatField(null=True, blank = True)
    expected_production_time = models.TimeField(default=None)
    expected_delivery_time = models.TimeField(null=True, blank = True)
    selected_vehicle_type = models.FloatField(null=True, blank = True)
    selected_vehicle_cost = models.FloatField(null=True, blank = True)
    real_production = models.TimeField(null=True, blank = True)
    real_delivery_time = models.TimeField(null=True, blank = True)

    @staticmethod
    def create_analyses(order, customer_coordinate, restaurant_id, route_cost, expected_production_time, real_prodution_time, expected_delivery_time):
        """Create_analysesitem is a function which is called when a new object of Analysesitem needs to be created."""

        obj = Analyses.objects.create(order=order, customer_coordinate=customer_coordinate
                    , restaurant_id=restaurant_id, route_cost=route_cost, expected_production_time=expected_production_time,
                    expected_delivery_time=expected_delivery_time, real_production=real_prodution_time)
        return obj


class Deliverers(models.Model):
    vehicle = models.ForeignKey(Vehicles, null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, null=True, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Orders, related_name='deliverers')
    capacity_available = models.PositiveBigIntegerField()
    busy_until = models.TimeField(default=datetime.now().replace(hour=0, minute=0, second=1),null=True, blank=True)


    @staticmethod
    def create_deliverer(vehicle, restaurants, order, capacity_available, busy_until):
        """Create_Deliverers is a function which is called when a new object of Analysesitem needs to be created."""
        obj = Deliverers.objects.create(vehicle=vehicle, restaurant=restaurants, capacity_available=capacity_available, busy_until=busy_until)

        obj.orders.add(order)
        return obj

    @staticmethod
    def add_order(id, order, capacity_available, busy_until, vehicle=None):
        """Create_Deliverers is a function which is called when a new object of Analysesitem needs to be created."""
        obj = Deliverers.objects.get(pk=id)
        obj.busy_until = busy_until
        obj.capacity_available = capacity_available

        if vehicle:
           obj.vehicle = vehicle 

        obj.orders.add(order)

        obj.save()

        return obj