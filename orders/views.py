from django.shortcuts import render, redirect
from .models import Orders,Restaurants, Results

from django.contrib import messages

from datetime import date, time, datetime, timedelta

# Create your views here.
def restaurants(request):

    active_order = Orders.objects.filter(state__isnull=True).exclude(pizza_amount=0).order_by('id')[0]
    results = Results.objects.get(order_id=active_order.id)

    all_restaurants = Restaurants.objects.all()
    
    type_of_meals = ['pizza_amount']
    basket = []
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket.append(('Pizza amount', active_order.pizza_amount))
    context = {
        "option1": int(results.first_restaurant),
        "option2": int(results.second_restaurant),
        "option3": int(results.third_restaurant),
        "results":results,
        "active_order":active_order,
        "basket":basket,
        "all_restaurants":all_restaurants,
    }

    return render(request, 'orders/restaurants.html', context)


def deliverer(request):
    active_order = Orders.objects.filter(state='R').exclude(pizza_amount=0).order_by('id')[0]

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


def restaurant_selection(request, restaurant_id):

    # Updating active order
    active_order = Orders.objects.filter(state__isnull=True).exclude(pizza_amount=0).order_by('id')[0]
    active_order.state = 'R'
    restaurant = Restaurants.objects.get(id=restaurant_id)
    active_order.selected_restaurant_id = restaurant
    active_order.save(update_fields=['selected_restaurant_id', 'state'])

    # Updating Restaurant time 
    restaurant = Restaurants.objects.get(id=restaurant_id)
    print(type(active_order.order_time))
    print("busy_until")
    if not restaurant.busy_until: 
        restaurant.busy_until = active_order.order_time + timedelta(minutes=active_order.production_time)
    elif restaurant.busy_until < active_order.order_time:
        restaurant.busy_until = active_order.order_time + timedelta(minutes=active_order.production_time)
    else:
        restaurant.busy_until = restaurant.busy_until + timedelta(minutes=active_order.production_time)
    print(type(restaurant.busy_until))

    messages.success(request, f'You have selected restaurant {restaurant.id}')
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

