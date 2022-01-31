from django.urls import path, include
from . import views
from orders.dash_apps.test_app import simpleexample

urlpatterns = [
    path('', views.restaurants, name='restaurants'),
    path('deliverer', views.deliverer, name='deliverer'),
    path('restaurant_selection/<int:option_id>', views.restaurant_selection, name='restaurant_selection'),
    path('search_view', views.search_view, name='search_view'),
    path('restaurant_info/<int:restaurant_id>', views.restaurant_info, name='restaurant_info')
]