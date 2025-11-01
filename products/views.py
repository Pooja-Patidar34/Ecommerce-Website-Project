from django.shortcuts import render,get_object_or_404
from products.models import Product,Category
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    else:
        category = None

    # Annotate products with stock status
    for product in products:
        product.is_out_of_stock = product.stock <= 0  # True if stock is 0 or less

    return render(request, 'products/products_list.html', {
        'categories': categories,
        'products': products,
        'selected_category': category
    })

