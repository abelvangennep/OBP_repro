from django.shortcuts import render
from .models import Orders

# Create your views here.
def orders(request):
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
