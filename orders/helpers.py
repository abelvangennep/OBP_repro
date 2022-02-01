from re import I

from .models import Orders,Restaurants, Results, Analyses, Deliverers, Vehicles

from datetime import date, time, datetime, timedelta
import pandas as pd


def calculate_production_time(restaurant, active_order, production_minutes):
    """"Calculate production time dependent on whether or not the Restaurant can immediately start"""

    if not restaurant.busy_until: 
        restaurant.busy_until = (datetime.combine(date(1,1,1), active_order.order_time) + production_minutes).time()
        real_prodution_time = production_minutes
    elif restaurant.busy_until < active_order.order_time:
        restaurant.busy_until = (datetime.combine(date(1,1,1), active_order.order_time) + production_minutes).time()
        real_prodution_time = production_minutes
    else:
        restaurant.busy_until = (datetime.combine(date(1,1,1), restaurant.busy_until) + production_minutes).time()
        real_prodution_time = datetime.combine(date.today(), restaurant.busy_until) - datetime.combine(date.today(), active_order.order_time)

    real_prodution_time = str(real_prodution_time)
    production_minutes = str(production_minutes)
    restaurant.save(update_fields=['busy_until'])

    return str(real_prodution_time), str(production_minutes)
    

def restaurant_id_production(option):
    results = Results.objects.get(order_id=get_active_order().id)

    if option == 1:
        return int(results.first_restaurant), results.first_route_cost, timedelta(minutes=results.first_restaurant_production_time), timedelta(minutes=results.first_duration_restaurant)

    elif option == 2:
        return int(results.second_restaurant), results.second_route_cost, timedelta(minutes=results.second_restaurant_production_time), timedelta(minutes=results.second_duration_restaurant)

    else:
        return int(results.third_restaurant), results.third_route_cost, timedelta(minutes=results.third_restaurant_production_time), timedelta(minutes=results.third_duration_restaurant)

def restaurant_id_merge(restaurant_id):
    results = Results.objects.get(order_id=get_active_order().id)

    if int(results.first_restaurant) == restaurant_id:
        return int(results.first_restaurant), results.first_route_cost, timedelta(minutes=results.first_restaurant_production_time), timedelta(minutes=results.first_duration_restaurant)

    elif int(results.second_restaurant) == restaurant_id:
        return int(results.second_restaurant), results.second_route_cost, timedelta(minutes=results.second_restaurant_production_time), timedelta(minutes=results.second_duration_restaurant)

    else:
        return int(results.third_restaurant), results.third_route_cost, timedelta(minutes=results.third_restaurant_production_time), timedelta(minutes=results.third_duration_restaurant)


def get_active_order():
    return Orders.objects.filter(state__isnull=True).exclude(pizza_amount=0).order_by('id')[0]


def minutes_still_busy(restaurant_id):
    order_time = get_active_order().order_time

    restaurant = Restaurants.objects.get(id=restaurant_id)

    if restaurant.busy_until:
        time = datetime.combine(date.today(), restaurant.busy_until) - datetime.combine(date.today(), order_time)
        if time.total_seconds() > 0:
            return f"Ready to start in: {int(time.total_seconds()/60)} minutes and {int(time.total_seconds()%60)} seconds"
    
    return "Ready to start!"


def deliverers_available(order_time, restaurant_id, capacity_needed):
    objects = Deliverers.objects.filter(restaurant_id=restaurant_id)
    available_deliverers = []

    if objects:
        for obj in objects:
            time = datetime.combine(date.today(), obj.busy_until) - datetime.combine(date.today(), order_time)
            if time.total_seconds() > 0 and obj.capacity_available > capacity_needed:
                available_deliverers.append(obj)
    
    return available_deliverers


def order_active(reastaurant_id, order_time):

    allocated_orders = Analyses.objects.filter(restaurant_id = reastaurant_id)
    active_order = []
    for order in allocated_orders:
        
        order_time_old_order = datetime.combine(date.min, Orders.objects.get(pk=order.order_id).order_time) - datetime.min
        prep_time = datetime.combine(date.min, order.real_production) - datetime.min

        order_time_new = datetime.combine(date.min, order_time) - datetime.min
        time = order_time_old_order + prep_time - order_time_new

        if time.total_seconds() > 0:
            active_order.append(order)
    return active_order
