from re import I
from django.shortcuts import render, redirect
from .models import Orders,Restaurants, Results, Analyses, Deliverers, Vehicles

from django.contrib import messages

from datetime import date, time, datetime, timedelta
import pandas as pd

from django.db.models import Q

# Create your views here.
def restaurants(request, restaurant_id=3):

    active_order = get_active_order()
    results = Results.objects.get(order_id=active_order.id)
    

    all_restaurants_pizza = Restaurants.objects.filter(~Q(pizza_parallel=0))
    i=0
    for restaurant in all_restaurants_pizza:
        if restaurant.restaurant_id_pizza:
            continue
        else:
            restaurant.restaurant_id_pizza = i
            i = i+1
            restaurant.save(update_fields=['restaurant_id_pizza'])



    option_1_id = Restaurants.objects.get(restaurant_id_pizza=int(results.first_restaurant))
    option_2_id = Restaurants.objects.get(restaurant_id_pizza=int(results.second_restaurant))
    option_3_id = Restaurants.objects.get(restaurant_id_pizza=int(results.third_restaurant))


    restaurant = Restaurants.objects.get(id=restaurant_id)
    orders_at_restaurant = order_active(restaurant_id, active_order.order_time)

    
    first_busy = minutes_still_busy(int(results.first_restaurant))
    second_busy = minutes_still_busy(int(results.second_restaurant))
    third_busy = minutes_still_busy(int(results.third_restaurant))

    first_deliverers = deliverers_available(active_order.order_time, int(results.first_restaurant))
    second_deliverers = deliverers_available(active_order.order_time, int(results.second_restaurant))
    third_deliverers = deliverers_available(active_order.order_time, int(results.third_restaurant))

    type_of_meals = ['pizza_amount']
    basket = []
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket.append(('Pizza amount', active_order.pizza_amount))


    context = {
        "first_deliverers": first_deliverers,
        "second_deliverers": second_deliverers,
        "third_deliverers": third_deliverers,
        "first_busy": first_busy,
        "second_busy": second_busy,
        "third_busy": third_busy,
        "option1": int(results.first_restaurant),
        "option_1_id": option_1_id,
        "option_2_id": option_2_id,
        "option_3_id": option_3_id,
        "option2": int(results.second_restaurant),
        "option3": int(results.third_restaurant),
        "results":results,
        "active_order":active_order,
        "basket":basket,
        "all_restaurants_pizza":all_restaurants_pizza,
        "restaurant": restaurant,
        "orders_at_restaurant": orders_at_restaurant,
    }

    return render(request, 'orders/restaurants.html', context)


def deliverer(request):
    active_order = get_active_order()

    type_of_meals = ['pizza_amount']
    basket = {}
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket['Pizza amount'] = active_order.pizza_amount
    context = {
        "active_order":active_order,
        "basket":basket,
    }

    return render(request, 'orders/deliverer.html', context)

def restaurant_info(request, restaurant_id):
    return restaurants(request, restaurant_id)


def restaurant_selection(request, option_id):

    restaurant_id, route_cost, production_minutes, expected_delivery_time = restaurant_id_production(option_id)
    active_order = get_active_order()

    orders_at_restaurant = order_active(restaurant_id, active_order.order_time)
    if orders_at_restaurant:
        deliverers_at_restaurant = deliverers_available(active_order.order_time, restaurant_id)
        
        type_of_meals = ['pizza_amount']
        basket = {}
        for meal in type_of_meals:
            if active_order.pizza_amount > 0:
                basket['Pizza amount'] = active_order.pizza_amount

        context = {
            "option_id":option_id,
            "deliverers_at_restaurant":deliverers_at_restaurant,
            "orders_at_restaurant":orders_at_restaurant,
            "active_order":active_order,
            "basket":basket,
        }

        return render(request, 'orders/merge.html', context)

    else:
        return non_merge(request, option_id)


def non_merge(request, option_id):
    restaurant_id, route_cost, production_minutes, expected_delivery_time = restaurant_id_production(option_id)
    active_order = get_active_order()

    active_order.state = 'R'
    restaurant = Restaurants.objects.get(restaurant_id_pizza=restaurant_id)
    active_order.selected_restaurant_id = restaurant
    active_order.save(update_fields=['selected_restaurant_id', 'state'])

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
    messages.success(request, f'You have selected restaurant {restaurant.id}')
    
    result = Results.objects.get(order_id=active_order.id)

    Analyses.create_analyses(active_order, result.customer_coordinate, restaurant.id, route_cost, production_minutes, real_prodution_time, str(expected_delivery_time))
    
    vehicle = Vehicles.objects.get(pk=result.first_vehicle_type)
    capacity = vehicle.capacity - active_order.pizza_amount


    Deliverers.create_deliverer(vehicle, restaurant, active_order, capacity, restaurant.busy_until)

    return redirect('restaurants')

def merge(request, deliverer_id):
    deliverer = Deliverers.objects.get(pk=deliverer_id)

    restaurant_id, route_cost, production_minutes, expected_delivery_time = restaurant_id_production(deliverer.restaurant_id)
    active_order = get_active_order()

    active_order.state = 'R'
    restaurant = Restaurants.objects.get(restaurant_id_pizza=restaurant_id)
    active_order.selected_restaurant_id = restaurant
    active_order.save(update_fields=['selected_restaurant_id', 'state'])

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
    messages.success(request, f'You have merged order {active_order.id}, with deliverer {deliverer.id}')
    
    result = Results.objects.get(order_id=active_order.id)
    ### Still to implement:
    # Discount route cost
    # Change production_time of prev order 
    Analyses.create_analyses(active_order, result.customer_coordinate, restaurant.id, route_cost, production_minutes, real_prodution_time, str(expected_delivery_time))
    
    capacity = deliverer.capacity_available - active_order.pizza_amount

    Deliverers.add_order(deliverer_id, active_order, capacity, restaurant.busy_until)

    return redirect('restaurants')


def search_view(request):
    if request.method == "POST":
        searched = request.POST["main_search_bar"]

        try:
            searched_order = Orders.objects.filter(id=searched).first()
            if searched_order:
                return render(request, 'orders/orders.html', {"active_order":searched_order})
        except:
            pass

        max = Orders.objects.all().order_by("-id")[0]
        min = Orders.objects.all().order_by("id")[0]
        return render(request, 'orders/orders.html', {"max":max, "min":min})

    return redirect('restaurants')

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


def deliverers_available(order_time, restaurant_id):
    objects = Deliverers.objects.filter(restaurant_id=restaurant_id)
    available_deliverers = []

    if objects:
        for obj in objects:
            time = datetime.combine(date.today(), obj.busy_until) - datetime.combine(date.today(), order_time)
            if time.total_seconds() > 0:
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

