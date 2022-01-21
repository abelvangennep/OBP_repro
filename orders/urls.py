from django.urls import path, include
from . import views
from orders.dash_apps.test_app import template

urlpatterns = [
    path('', views.orders, name='orders'),
    path('deliverer', views.deliverer, name='deliverer'),
    path('restaurant_selection/<int:restaurant_id>', views.restaurant_selection, name='restaurant_selection')
]