from django.db import models
from django.contrib.auth.models import User
from products.models import*

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
         