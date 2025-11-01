import logging
import hmac, hashlib, json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from cart.models import CartItem
from order.models import Order
import razorpay
from django.db import transaction
from django.db.models import F
from products.models import Product
# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Get custom logger
logger = logging.getLogger("payments")


@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    # Create order in DB

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        payment_status="Pending"
    )

    # Create Razorpay order
    razorpay_order = client.order.create({
        "amount": int(total * 100),
        "currency": "INR",
        
        "payment_capture": 1
    })

    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    logger.info(f"Checkout initiated for Order {order.id}, Razorpay Order: {razorpay_order['id']}")

    context = {
        "order": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": razorpay_order["id"],
        "amount": total * 100,
        "currency": "INR"
    }
    return render(request, "order/checkout.html", context)

@csrf_exempt
def razorpay_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    payload = request.body
    signature = request.headers.get("X-Razorpay-Signature")
    secret = settings.RAZORPAY_WEBHOOK_SECRET

    logger.debug(f"Webhook payload: {payload}")
    logger.debug(f"Signature received: {signature}")

    generated_signature = hmac.new(
        secret.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(generated_signature, signature):
        logger.error("Invalid signature received in webhook")
        return HttpResponseBadRequest("Invalid signature")

    try:
        data = json.loads(payload.decode("utf-8"))
        event = data.get("event")
        order_id = data["payload"]["payment"]["entity"]["order_id"]
        order = Order.objects.get(razorpay_order_id=order_id)
    except Exception as e:
        logger.exception(f"Error processing webhook: {str(e)}")
        return HttpResponseBadRequest("Error processing webhook")

    if event == "payment.captured":
        with transaction.atomic():
            # Lock all products in the user's cart
            cart_items = CartItem.objects.filter(user=order.user).select_related("product")
            product_ids = [item.product.id for item in cart_items]

            # Lock the product rows
            products = Product.objects.select_for_update().filter(id__in=product_ids)
            products_map = {p.id: p for p in products}

            for item in cart_items:
                product = products_map[item.product.id]

                if product.stock < item.quantity:
                    logger.warning(f"Not enough stock for {product.name}")
                    raise Exception(f"{product.name} is out of stock")

                # Safely decrement stock
                product.stock = F("stock") - item.quantity
                product.save(update_fields=["stock"])

            # Clear the user's cart
            cart_items.delete()

            # Update order
            order.payment_status = "Paid"
            order.save()

        logger.info(f"Payment captured for Order {order.id}, stock updated and cart cleared")

    elif event == "payment.failed":
        order.payment_status = "Failed"
        order.save()
        logger.warning(f"Payment failed for Order {order.id}")

    else:
        logger.warning(f"Unhandled webhook event: {event}")

    return HttpResponse(status=200)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    logger.debug(f"Fetched {orders.count()} orders for user {request.user}")
    return render(request, "order/history.html", {"orders": orders})
