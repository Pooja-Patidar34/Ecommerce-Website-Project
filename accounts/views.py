from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid Username'}, status=400)
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        user = authenticate(request, username=username, password=password)
        if user is None:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Invalid Password'}, status=400)
            messages.error(request, 'Invalid Password')
            return redirect('/login/')

        login(request, user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': '/'})
        return redirect('/')

    return render(request, 'accounts/login.html')

                        
def register_page(request):
          if request.method=='POST':
                first_name=request.POST.get('first_name')
                last_name=request.POST.get('last_name')
                username=request.POST.get('username')
                password=request.POST.get('password')
                user=User.objects.filter(username=username)
                if user.exists():
                        messages.info(request,'Username Already Taken!!!')
                        return redirect('/register/')
                user=User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username
                )
                user.set_password(password)
                user.save()
                messages.info(request,'Account Created Successfully')
                return redirect('/register/')
          return render(request,'accounts/register.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login_page')