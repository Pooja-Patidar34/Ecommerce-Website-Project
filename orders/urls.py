from django.urls import path
from orders.views import place_order,payment_success,checkout_view,order_history

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('place/',place_order,name='place_order'),
    path('payment/success/',payment_success,name='payment_success'),
    path("history/", order_history, name="order_history"),
]
