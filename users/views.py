
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import logout
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
import json

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'users/index.html')

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

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_active = False  # Disable account until email is verified
        user.save()

        Profile.objects.create(user=user, role=role)

        # Store the email in the session for OTP verification
        request.session['verification_email'] = email

        # Send OTP email
        try:
            send_otp_email(email)
        except Exception as e:
            messages.error(request, f"Error sending OTP: {e}")
            return redirect('register')

        messages.success(request, "Registered successfully. Please verify your email.")
        return redirect('verification')

    return render(request, 'users/register.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # email is used as username
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')  # Make sure your login view is named 'login'

from .forms import ProfileUpdateForm


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            # Save User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # Save Profile model fields
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })

    return render(request, 'users/profile.html', {'form': form})




OTP_STORAGE = {}

def send_otp_email(user_email):
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    OTP_STORAGE[user_email] = otp  # Save OTP temporarily (you should save it in a session or database in production)

    # Send the OTP to the user's email
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}.',
        'from@example.com',  # Use a real email address
        [user_email],
        fail_silently=False,
    )


import json
from django.http import JsonResponse


def verification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            otp = data.get('otp')
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'})

        user_email = request.session.get('verification_email')

        if not user_email:
            return JsonResponse({'success': False, 'message': 'No email found in session.'})

        if OTP_STORAGE.get(user_email) == otp:
            try:
                user = User.objects.get(email=user_email)
                user.is_active = True
                user.save()
                del OTP_STORAGE[user_email]
                auth_login(request, user)
                return JsonResponse({'success': True, 'message': 'OTP verified successfully! Redirecting...', 'redirect_url': '/index/'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User does not exist.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP.'})

    # Return HTML only for GET
    return render(request, 'users/verification.html')
