from re import I
from django.shortcuts import render, redirect
from .models import Orders,Restaurants, Results, Analyses, Deliverers, Vehicles
from .helpers import calculate_production_time, restaurant_id_production, restaurant_id_merge, get_active_order, minutes_still_busy, deliverers_available, order_active
from django.contrib import messages

from datetime import date, time, datetime, timedelta
import pandas as pd

from django.db.models import Q

def restaurants(request, restaurant_id=3):
    """ This view renders the restaurant.html page, it uses multiple helper functies to collect statistics"""

    # Retrieve the order, which is currently being evaluated (FIFO)
    active_order = get_active_order()

    # Retrieve corresponding upfront calculated statistics
    results = Results.objects.get(order_id=active_order.id)
    
    # Check which restaurants produce pizza 
    all_restaurants_pizza = Restaurants.fill_id_pizza()

    # Retrieve the objects corresponding to suggestions of the results table
    option_1_id = Restaurants.objects.get(restaurant_id_pizza=int(results.first_restaurant))
    option_2_id = Restaurants.objects.get(restaurant_id_pizza=int(results.second_restaurant))
    option_3_id = Restaurants.objects.get(restaurant_id_pizza=int(results.third_restaurant))

    # Retrieve selected Restaurant in restaurant information box, default=3 
    restaurant = Restaurants.objects.get(id=restaurant_id)
    orders_at_restaurant = order_active(restaurant_id, active_order.order_time)

    # Check whether restaurants are still working on an order
    first_busy = minutes_still_busy(int(results.first_restaurant))
    second_busy = minutes_still_busy(int(results.second_restaurant))
    third_busy = minutes_still_busy(int(results.third_restaurant))

    # Check which deliverers did not yet leave the restaurant and have capacity left
    first_deliverers = deliverers_available(active_order.order_time, int(results.first_restaurant), active_order.pizza_amount)
    second_deliverers = deliverers_available(active_order.order_time, int(results.second_restaurant), active_order.pizza_amount)
    third_deliverers = deliverers_available(active_order.order_time, int(results.third_restaurant), active_order.pizza_amount)

    # Fill the basket to show in order information
    type_of_meals = ['pizza_amount']
    basket = []
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
    """Renders the page the deliverer """

    return render(request, 'orders/deliverer.html')

def restaurant_info(request, restaurant_id):
    """Runs the restaurant page with a different Restaurant information block """

    return restaurants(request, restaurant_id)


def restaurant_selection(request, option_id):
    """Function is called when scheduler clicks an option """

    # Retrieve the active order and restaurant_id clicked
    restaurant_id, route_cost, production_minutes, expected_delivery_time = restaurant_id_production(option_id)
    active_order = get_active_order()

    deliverers_at_restaurant = deliverers_available(active_order.order_time, restaurant_id, active_order.pizza_amount)
    
    # Check whether their already is a deliverer available to bring the order
    if deliverers_at_restaurant:
        orders_at_restaurant = order_active(restaurant_id, active_order.order_time)
        
        # Fill the basket to show in order information
        type_of_meals = ['pizza_amount']
        basket = []
        basket.append(('Pizza amount', active_order.pizza_amount))

        context = {
            "option_id":option_id,
            "deliverers_at_restaurant":deliverers_at_restaurant,
            "orders_at_restaurant":orders_at_restaurant,
            "active_order":active_order,
        }

        return render(request, 'orders/merge.html', context)

    else:
        return non_merge(request, option_id)


def non_merge(request, option_id):
    """This function is called when scheduler selects option, which does not have merging availabilities"""

    # Retrieve the active order and the production related information
    restaurant_id, route_cost, production_minutes, expected_delivery_time = restaurant_id_production(option_id)
    active_order = get_active_order()
    restaurant = Restaurants.objects.get(restaurant_id_pizza=restaurant_id)

    # Change DB fields of the active order
    active_order.state = 'R'
    active_order.selected_restaurant_id = restaurant
    active_order.save(update_fields=['selected_restaurant_id', 'state'])

    # Calculate the new prouction time
    real_prodution_time, production_minutes = calculate_production_time(restaurant, active_order, production_minutes)
    
    # Save the findings in an Analyses model
    result = Results.objects.get(order_id=active_order.id)
    Analyses.create_analyses(active_order, result.customer_coordinate, restaurant.id, route_cost, production_minutes, real_prodution_time, str(expected_delivery_time))
    
    # Create a new deliverer
    vehicle = Vehicles.objects.get(pk=result.first_vehicle_type)
    capacity = vehicle.capacity - active_order.pizza_amount
    deliverer = Deliverers.create_deliverer(vehicle, restaurant, active_order, capacity, restaurant.busy_until)

    # Return a succeess message
    messages.success(request, f'You have selected restaurant {restaurant.id}, deliverer {deliverer.id} is assigned to this order')

    return redirect('restaurants')

def merge(request, deliverer_id):
    """When scheduler decides to merge orders """

    # Retrieve the active order and the production related information
    deliverer = Deliverers.objects.get(pk=deliverer_id)
    restaurant_id, route_cost, production_minutes, expected_delivery_time = restaurant_id_production(deliverer.restaurant_id)
    active_order = get_active_order()

    # Change DB fields of the active order
    active_order.state = 'R'
    restaurant = Restaurants.objects.get(restaurant_id_pizza=restaurant_id)
    active_order.selected_restaurant_id = restaurant
    active_order.save(update_fields=['selected_restaurant_id', 'state'])

    # Calculate the new prouction time 
    real_prodution_time, production_minutes = calculate_production_time(restaurant, active_order, production_minutes)

    # Save all the data in a model, which keeps track of the findings
    Analyses.create_analyses(active_order, Results.objects.get(order_id=active_order.id).customer_coordinate, restaurant.id, route_cost, production_minutes, real_prodution_time, str(expected_delivery_time))
    
    # Add the order to existing deliverer
    Deliverers.add_order(deliverer_id, active_order, deliverer.capacity_available - active_order.pizza_amount, restaurant.busy_until)

    messages.success(request, f'You have merged order {active_order.id}, with deliverer {deliverer.id}')

    return redirect('restaurants')


def search_view(request):
    """This view makes searchin for potential orders possible"""

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

