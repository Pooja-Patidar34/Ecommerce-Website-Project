from django.shortcuts import render,redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from cart.models import *
from orders.models import *
from products.models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
import razorpay

client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

@login_required
def checkout_view(request):
    user = request. user
    cart_items = CartItem.objects.filter(user=user)                           

    total = sum(item.get_total_price() for item in cart_items)
    total_paise = int(total * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        "amount": total_paise,
        "currency": "INR", 
        "payment_capture": "1"
    })
    context = {
        "cart_items": cart_items,
        "total": total,
        "razorpay_order": razorpay_order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def place_order(request):
          cart_items=CartItem.objects.filter(user=request.user)
          if not cart_items:
                  return redirect('product_list')
          
          total_amount=sum(item.get_total_price()for item in cart_items)
          print(total_amount)
          total_amount_paise=int(total_amount*100)

          razorpay_order=client.order.create({
                  "amount":total_amount_paise,
                  "currency":"INR",
                  "payment_capture":"1"
          })

          request.session['razorpay_order_id']=razorpay_order['id']
          return render(request,'orders/checkout.html',{
                  'cart_items':cart_items,
                  'total':total_amount,
                  'razorpay_order':razorpay_order,
                  'razorpay_key':settings.RAZORPAY_KEY_ID
})

@csrf_exempt
@login_required
@transaction.atomic
def payment_success(request):
    if request.method == "POST":
        # Razorpay sends details after payment
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
        except:
            return render(request, "orders/payment_failed.html")

        # ✅ Create order
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items:
            return redirect('product_list')

        order = Order.objects.create(
            user=request.user,
            is_paid=True,
            razorpay_order_id=order_id, 
            razorpay_payment_id=payment_id
        )
        
        for item in cart_items:
            if item.product.stock < item.quantity:
                return render(request,'cart/view_cart.html',{'error':'Insufficient Stock'})
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.stock -= item.quantity
            item.product.save()
        cart_items.delete()

        return redirect("order_history")
    return HttpResponseBadRequest("Invalid request")


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})



