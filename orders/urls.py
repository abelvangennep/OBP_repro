from django.urls import path, include
from . import views
from orders.dash_apps.test_app import simpleexample

urlpatterns = [
    path('', views.restaurants, name='restaurants'),
    path('deliverer', views.deliverer, name='deliverer'),
    path('restaurant_selection/<int:option_id>', views.restaurant_selection, name='restaurant_selection'),
    path('merge/<int:deliverer_id>', views.merge, name='merge'),
    path('non_merge/<int:option_id>', views.non_merge, name='Non_merge'),
    path('search_view', views.search_view, name='search_view'),
    path('restaurant_info/<int:restaurant_id>', views.restaurant_info, name='restaurant_info')
]