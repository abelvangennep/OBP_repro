from django.shortcuts import render
from .models import Orders,Restaurants

# Create your views here.
def orders(request):

    if request.method=="POST":
        active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]
        restaurant = Restaurants.objects.get(id=0)
        active_order.state = 'R'
        active_order.selected_restaurant_id = restaurant
        active_order.save(update_fields=['selected_restaurant_id', 'state'])

    active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]

    



    type_of_meals = ['pizza_amount']
    basket = []
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket.append(('Pizza amount', active_order.pizza_amount))
    context = {
        "active_order":active_order,
        "basket":basket,
    }
    




    return render(request, 'orders/orders.html', context)

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