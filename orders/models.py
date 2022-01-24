from django.db import models

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
    mon_open = models.DateTimeField(default=None)
    mon_close = models.DateTimeField(default=None)
    tue_open = models.DateTimeField(default=None)
    tue_close = models.DateTimeField(default=None)
    wed_open = models.DateTimeField(default=None)
    wed_close = models.DateTimeField(default=None)
    thu_open = models.DateTimeField(default=None)
    thu_close = models.DateTimeField(default=None)
    fri_open = models.DateTimeField(default=None)
    fri_close = models.DateTimeField(default=None)
    sat_open = models.DateTimeField(default=None)
    sat_close = models.DateTimeField(default=None)
    sun_open = models.DateTimeField(default=None)
    sun_close = models.DateTimeField(default=None)



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
    order_time = models.DateTimeField()
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

    def __str__(self):
        return f"{self.id}"


class Results(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    customer_coordinate = models.FloatField(null=True, blank = True)
    first_restaurant = models.FloatField(null=True, blank = True)
    first_duration_restaurant = models.FloatField(null=True, blank = True)
    first_distance_restaurant = models.FloatField(null=True, blank = True)
    firts_route_cost = models.FloatField(null=True, blank = True)
    second_restaurante = models.FloatField(null=True, blank = True)
    second_duration_restaurant = models.FloatField(null=True, blank = True)
    second_distance_restaurant = models.FloatField(null=True, blank = True)
    second_route_cost = models.FloatField(null=True, blank = True)
    third_restaurant = models.FloatField(null=True, blank = True)
    third_duration_restaurant = models.FloatField(null=True, blank = True)
    third_distance_restaurant = models.FloatField(null=True, blank = True)
    third_route_cost = models.FloatField(null=True, blank = True)
    pizza_order_amount = models.FloatField(null=True, blank = True)
    first_restaurant_production_time = models.FloatField(null=True, blank = True)
    second_restaurant_production_time = models.FloatField(null=True, blank = True)
    third_restaurant_production_time = models.FloatField(null=True, blank = True)
    first_restaurant_capacity = models.FloatField(null=True, blank = True)
    second_restaurant_capacity = models.FloatField(null=True, blank = True)
    third_restaurant_capacity = models.FloatField(null=True, blank = True)
    first_vehicle_type = models.FloatField(null=True, blank = True)
    first_vehicle_cost = models.FloatField(null=True, blank = True)
    second_vehicle_type = models.FloatField(null=True, blank = True)
    second_vehicle_cost = models.FloatField(null=True, blank = True)
    third_vehicle_type = models.FloatField(null=True, blank = True)
    third_vehicle_cost = models.FloatField(null=True, blank = True)
    first_total_cost_restaurant = models.FloatField(null=True, blank = True)
    second_total_cost_restaurant = models.FloatField(null=True, blank = True)
    third_total_cost_restaurant = models.FloatField(null=True, blank = True)



