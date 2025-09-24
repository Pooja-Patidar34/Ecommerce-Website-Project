from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Category,Product
from .forms import CategoryForm,ProductForm
from cart.models import CartItem
from orders.models import Order,OrderItem,Transaction

User = get_user_model()

def is_superuser(user):
    return user.is_superuser

def is_admin(user):
    return user.is_staff 

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid email or password, or you are not an admin.")
            return redirect("admin_login")
    return render(request, "admin/admin_login.html")

@login_required
def admin_dashboard(request):
    return render(request,'admin/dashboard.html')

def all_users(request):
    users=User.objects.all()
    return render(request,'admin/all_users.html',{'users':users})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def block_user(request, user_id):
    user=get_object_or_404(User, id=user_id)

    if request.user == user:
        messages.error(request,"You can't Block yourself")
        return redirect('all_users')
    if user.is_superuser:
        messages.error(request,"You can't Block Superuser")
        return redirect('all_users')
    
    user.is_active=False
    user.save()
    messages.success(request,f"User {user.username} has been Block successfully !!")
    return redirect('all_users')

def unblock_user(request, user_id):
    user=get_object_or_404(User, id=user_id)
    user.is_active=True
    user.save()
    messages.success(request,f"User {user.username} has been Unblock successfully !!")
    return redirect('all_users')

def show_block_users(request):
    users=User.objects.filter(is_active=False)
    return render(request,'admin/show_block_users.html',{'users':users})

def show_category(request):
    categories=Category.objects.all()
    return render(request,'admin/show_category.html',{'categories':categories})

def delete_category(request,pk):
    categories=get_object_or_404(Category,pk=pk)
    categories.delete()
    messages.success(request,'Category Deleted Successfully')
    return redirect('show_category')

def edit_category(request,pk):
    categories=get_object_or_404(Category,pk=pk)

    if request.method=='POST':
        form=CategoryForm(request.POST, instance=categories)
        if form.is_valid():
            form.save()
            messages.success(request,'Category Updated Succesfully')
            return redirect('show_category')
    else:
            form=CategoryForm(instance=categories)
    return render(request,'admin/edit_category.html',{'form':form})

def show_products(request):
    products=Product.objects.all()
    return render(request,'admin/show_products.html',{'products':products})

def delete_product(request,pk):
    products=get_object_or_404(Product,pk=pk)
    products.delete()
    messages.success(request,'Product deleted Successfully')
    return redirect('show_products')

def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST, request.FILES)
        form.is_valid()
        form.save()
        messages.success(request,'Category Added Successfully')
        return redirect('show_category')
    else:
        form=CategoryForm()
    return render(request,'admin/add_category.html',{'form':form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        if form.is_valid():                               
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('show_products')  
        else:
            messages.error(request, "Please correct the errors below.") 
    else:
        form = ProductForm()
    return render(request, 'admin/add_product.html', {'form': form})


def edit_product(request,pk):
    products=get_object_or_404(Product,pk=pk)

    if request.method=='POST':
        form=ProductForm(request.POST, instance=products)
        if form.is_valid():
            form.save()
            messages.success(request,'Product Updated Succesfully')
            return redirect('show_products')
    else:
            form=ProductForm(instance=products)
    return render(request,'admin/edit_product.html',{'form':form})

@login_required
def cartview(request):
        cart_items=CartItem.objects.all().order_by('-created_at')
        total=sum([item.get_total_price() for item in cart_items])
        return render(request,'admin/cartview.html',{'cart_items':cart_items,'total':total})

@login_required
def removefromcart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_superuser:
        cart_item = CartItem.objects.filter(product=product).first()
    else:
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cartview')

def order_transactions(request):
    transactions=Transaction.objects.all().order_by('created_at')
    return render(request,'admin/order_transactions.html',{'transactions':transactions})
