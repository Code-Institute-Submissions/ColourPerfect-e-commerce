from django.urls import path
from wishlist.views import wishlist, add_to_wishlist, delete_wishlist_item


urlpatterns = [
    path('', wishlist, name='wishlist'),
    path('add/<product_id>', add_to_wishlist, name='add_to_wishlist'),
    path('delete/<item_id>', delete_wishlist_item, name='delete_wishlist_item'),



]