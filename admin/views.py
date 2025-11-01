from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout,get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Category,Product
from .forms import CategoryForm,ProductForm,RoleForm
from cart.models import CartItem
from order.models import Order
from accounts.models import Role,RolePermissions,RoleUser,Permission
from .decorators import superuser_required,permission_required

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

        if user is not None:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("admin_login")

    return render(request, "admin/admin_login.html")

User = get_user_model()

@login_required
def create_user(request):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to create users.")
        return redirect("admin_dashboard")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")


        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("create_user")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("create_user")

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        messages.success(request, "User created successfully!")
        return redirect("all_users") 
    return render(request, "admin/create_user.html")

@permission_required(module="user management", action="edit")
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect('all_users') 
    context = {
        "user": user
    }
    return render(request, "admin/edit_user.html", context)

@login_required
def admin_dashboard(request):
    role_user = RoleUser.objects.filter(user=request.user).first()
    return render(request, 'admin/dashboard.html', {'role_user': role_user})

@permission_required(module="user management", action="view")
def all_users(request):
    users=User.objects.all()
    return render(request,'admin/all_users.html',{'users':users})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@permission_required(module="user management", action="edit")
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

@permission_required(module="user management", action="edit")
def unblock_user(request, user_id):
    user=get_object_or_404(User, id=user_id)
    user.is_active=True
    user.save()
    messages.success(request,f"User {user.username} has been Unblock successfully !!")
    return redirect('all_users')

@permission_required(module="user management", action="view")
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


@permission_required(module="products", action="view")
def show_products(request):

    role_user = RoleUser.objects.filter(user=request.user).first()
    if role_user:
        print("Role:", role_user.role.rname)
    else:
        print("No role assigned to this user")

    products = Product.objects.all()

    return render(request, 'admin/show_products.html', {'products': products})

@permission_required(module="products", action="delete")
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
        messages.success(request,'Category Added Successfully!')
        return redirect('show_category')
    else:
        form=CategoryForm()
    return render(request,'admin/add_category.html',{'form':form})

@permission_required(module="products", action="create")
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)   
        if form.is_valid():                               
            form.save()
            messages.success(request, "Product added Successfully!")
            return redirect('show_products')  
        else:
            messages.error(request, "Please correct the errors below.") 
    else:
        form = ProductForm()
    return render(request, 'admin/add_product.html', {'form': form})

@permission_required(module="products", action="edit")
def edit_product(request,pk):
    products=get_object_or_404(Product,pk=pk)

    if request.method=='POST':
        form=ProductForm(request.POST, instance=products)
        if form.is_valid():
            form.save()
            messages.success(request,'Product Updated Successfully !')
            return redirect('show_products')
    else:
            form=ProductForm(instance=products)
    return render(request,'admin/edit_product.html',{'form':form})

@permission_required(module="carts", action="view")
@login_required
def cartview(request):
        cart_items=CartItem.objects.all().order_by('-created_at')
        total=sum([item.get_total_price() for item in cart_items])
        return render(request,'admin/cartview.html',{'cart_items':cart_items,'total':total})

@permission_required(module="carts", action="delete")
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

@login_required
@permission_required(module="orders", action="view")
def order(request):
    order = Order.objects.all().order_by('-created_at')
    return render(request,'admin/all_orders.html',{'order':order})

@superuser_required
def create_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()

    return render(request, "admin/create_role.html", {"form": form})


def role_list(request):
    roles = Role.objects.all().order_by('-id')
    print("ROLES ==> ", roles) 
    
    return render(request, "admin/rolelist.html", {"roles": roles})


@superuser_required
def assign_role(request):
    users=User.objects.all()
    roles=Role.objects.all()

    if request.method=="POST":
        user_id=request.POST.get("user")
        role_id=request.POST.get("role")

        user=User.objects.get(id=user_id)
        role=Role.objects.get(id=role_id)

        if not RoleUser.objects.filter(user=user,role=role).exists():
            RoleUser.objects.create(user=user,role=role)
            return redirect('assigned_roles')

        return redirect('assign_role')
    return render(request,'admin/assign_role.html',{'users':users,'roles':roles})

@superuser_required
def assigned_roles(request):
    assigned = RoleUser.objects.select_related('user', 'role')
    return render(request, "admin/assigned_roles.html", {"assigned": assigned})

def permission_list_create(request):
    permissions = Permission.objects.all().order_by("-id")

    if request.method == "POST":
        type_val = request.POST.get("type")
        path = request.POST.get("path")
        module = request.POST.get("module")

        Permission.objects.create(
            type=type_val,
            path=path if type_val == "path" else None,
            module=module if type_val == "module" else None
        )
        return redirect("permission_list_create")

    return render(request, "admin/permission_list_create.html", {"permissions": permissions})

    
from django.urls import reverse

def assign_role_permissions(request):
    roles = Role.objects.all()
    permissions = Permission.objects.all()
    selected_role_id = request.GET.get("role")

    role = None

    if selected_role_id:
        role = Role.objects.get(id=selected_role_id)

        role_perms = RolePermissions.objects.filter(role=role)
        perm_map = {rp.permission.id: rp for rp in role_perms}

        for perm in permissions:
            perm.rp = perm_map.get(perm.id, None)

    if request.method == "POST":
        role_id = request.POST.get("role")
        role = Role.objects.get(id=role_id)

        for perm in permissions:
            rp, created = RolePermissions.objects.get_or_create(role=role, permission=perm)

            rp.has_view = bool(request.POST.get(f"view_{perm.id}"))
            rp.has_create = bool(request.POST.get(f"create_{perm.id}"))
            rp.has_edit = bool(request.POST.get(f"edit_{perm.id}"))
            rp.has_delete = bool(request.POST.get(f"delete_{perm.id}"))
            rp.save()

        return redirect(f"{reverse('assign_role_permissions')}?role={role_id}")

    return render(request, "admin/assign_permission.html", {
        "roles": roles,
        "permissions": permissions,
        "role": role,
        "selected_role_id": selected_role_id
    })
