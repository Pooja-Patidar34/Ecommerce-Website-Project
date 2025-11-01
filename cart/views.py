from django.shortcuts import render,redirect,get_object_or_404
from cart.models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

@login_required

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product_list") 

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect("view_cart")

@login_required
def view_cart(request):
        items=CartItem.objects.filter(user=request.user)
        total=sum([item.get_total_price() for item in items])
        return render(request,'cart/view_cart.html',{'cart_items':items,'total':total})

@login_required
def remove_from_cart(request,product_id):
     product=get_object_or_404(Product,id=product_id)
     cart_item=CartItem.objects.filter(user=request.user,product=product).first()
     if cart_item:
          cart_item.delete()
     return redirect('view_cart')

@login_required
def get_cart_count(request):
     count=CartItem.objects.filter(user=request.user).count()
     return JsonResponse({'count':count})

@login_required
def update_cart_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    return redirect('view_cart')
