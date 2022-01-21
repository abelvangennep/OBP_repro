from django.shortcuts import render, redirect
from .models import Orders,Restaurants

from django.contrib import messages

# Create your views here.
def restaurants(request):

    active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]

    all_restaurants = Restaurants.objects.all()
    for restaurant in all_restaurants:
        print(restaurant.id)


    



    type_of_meals = ['pizza_amount']
    basket = []
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket.append(('Pizza amount', active_order.pizza_amount))
    context = {
        "active_order":active_order,
        "basket":basket,
        "all_restaurants":all_restaurants,
    }

    return render(request, 'orders/restaurants.html', context)


def deliverer(request):
    active_order = Orders.objects.filter(state='R').order_by('id')[0]

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

    active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]
    restaurant = Restaurants.objects.get(id=restaurant_id)
    active_order.state = 'R'
    active_order.selected_restaurant_id = restaurant
    active_order.save(update_fields=['selected_restaurant_id', 'state'])
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
