from django.urls import path
from basket.views import basket, add_to_basket, adjust_quantity, delete_item


urlpatterns = [
    path('', basket, name='basket'),
    path('add/<product_id>', add_to_basket, name='add_to_basket'),
    path('adjust', adjust_quantity, name='adjust_quantity'),
    path('delete/<item_id>', delete_item, name='delete'),



]