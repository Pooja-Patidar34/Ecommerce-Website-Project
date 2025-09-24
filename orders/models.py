from django.db import models
from django.contrib.auth.models import User
from products.models import*
from django.conf import settings
from orders.models import *


class Order(models.Model):
          user=models.ForeignKey(User ,on_delete=models.CASCADE)
          created_at=models.DateTimeField(auto_now_add=True)
          is_paid=models.BooleanField(default=False)
          razorpay_order_id=models.CharField(max_length=100, null=True,blank=True)
          razorpay_payment_id=models.CharField(max_length=100, null=True,blank=True)

          def __str__(self):
           return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
         order=models.ForeignKey(Order,  on_delete=models.CASCADE,related_name="items")
         product=models.ForeignKey(Product, on_delete=models.CASCADE)
         quantity=models.PositiveIntegerField()

         def get_total_price(self):
                 return self.product.price*self.quantity

class Transaction(models.Model):
    STATUS_CHOICES = (
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default="INR")

    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Txn {self.id} | Order {self.order.id} | {self.status}"
