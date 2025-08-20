from django.contrib import admin
from orders.models import *

admin.site.register(Order)
admin.site.register(OrderItem)