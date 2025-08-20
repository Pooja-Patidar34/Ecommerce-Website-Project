from django.urls import path
from cart.views import view_cart,add_to_cart,remove_from_cart,get_cart_count,update_cart_quantity

urlpatterns = [
    path('add/<int:product_id>/',add_to_cart,name='add_to_cart'),
    path('',view_cart,name='view_cart'),
    path('remove/<int:product_id>',remove_from_cart,name='remove_from_cart'),
    path('count/',get_cart_count, name='get_cart_count'),
    path('update-quantity/<int:item_id>/<str:action>/',update_cart_quantity,name='update_cart_quantity')
]
