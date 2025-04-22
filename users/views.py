from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Profile
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        Profile.objects.create(user=user, role=role)
        messages.success(request, "Registered successfully. Please log in.")
        return redirect('login')

    return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # email is used as username
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # Make sure your login view is named 'login'
