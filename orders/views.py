from django.shortcuts import render
from .models import Orders,Restaurants

# Create your views here.
def orders(request):

    if request.method=="POST":
        print("Hæææææ")
        active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]
        print(active_order)
        restaurant = Restaurants.objects.get(id=0)
        active_order.state = 'R'
        active_order.selected_restaurant_id = restaurant
        active_order.save(update_fields=['selected_restaurant_id', 'state'])

    active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]

    



    type_of_meals = ['pizza_amount']
    basket = {}
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket['Pizza amount'] = active_order.pizza_amount
    context = {
        "active_order":active_order,
        "basket":basket,
    }
    




    return render(request, 'orders/orders.html', context)

def deliverer(request):
    active_order = Orders.objects.filter(state__isnull=True).order_by('id')[0]

    type_of_meals = ["pizza's   "]
    basket = []
    for meal in type_of_meals:
        if active_order.pizza_amount > 0:
            basket.append((meal, active_order.pizza_amount))
    print(basket)
    context = {
        "active_order":active_order,
        "basket": basket,
        "order_status": "Not yet subjected to Restaurant",
    }



    return render(request, 'orders/orders.html', context)
