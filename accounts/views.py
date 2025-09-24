from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

User = get_user_model()

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if user exists in DB
            user_obj = User.objects.get(username=username)
            
            if not user_obj.is_active:
                messages.error(request, 'You are Blocked')
                return render(request, 'accounts/login.html')
        except User.DoesNotExist:
            user_obj = None

        # Authenticate only if user is not blocked
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')

def register_page(request):
          if request.method=='POST':
                first_name=request.POST.get('first_name')
                last_name=request.POST.get('last_name')
                email=request.POST.get('email')
                username=request.POST.get('username')
                password=request.POST.get('password')

                user=User.objects.filter(username=username)
                if user.exists():
                        messages.error(request,'Username Already Taken!!!')
                        return redirect('register_page')
                user=User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        username=username,
                )
                user.set_password(password)
                user.save()
                messages.info(request,'Account Created Successfully')
                return redirect('register_page')
          return render(request,'accounts/register.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login_page')