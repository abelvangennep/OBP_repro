from django.shortcuts import render
from .models import Orders

# Create your views here.
def orders(request):
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