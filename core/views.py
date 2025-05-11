from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('index')  # 'index' should be a named URL for index.html in users app
    return render(request, 'core/home.html')
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings

def help_page(request):
    submitted = False
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Enhanced message body
        full_message = f"""
        You have received a new support request from MomentsMaker:

        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        send_mail(
            subject=f"Support Request from {name}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,  # Safe default sender
            recipient_list=['mdmohhemedabdullah@gmail.com'],
            fail_silently=False,
        )
        submitted = True

    return render(request, 'core/help.html', {'submitted': submitted})

def about_view(request):
    return render(request, 'core/about.html')