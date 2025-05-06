"""
URL configuration for moments_maker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import settings
from django.conf.urls.static import static

from django.urls import path
from core import views as c_views
from users import views as u_views
from services import views as s_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',c_views.home, name = 'home'),
    path('help/', c_views.help_page, name='help'),
    path('about/', c_views.about_view, name='about'),

    path('index/', u_views.index, name='index'),
    path('login/',u_views.login, name = 'login'),
    path('register/',u_views.register, name = 'register'),
    path('logout/', u_views.logout_view, name='logout'),
    path('profile/',u_views.profile, name = 'profile'),
    path('verification/', u_views.verification, name='verification'),


    path('services/', s_views.services, name = 'services'),
    path('search_results/', s_views.search_results, name='search_results'),
    path('services/provider/<int:pk>/', s_views.provider_detail, name='provider_detail'),

    path('cart/', s_views.cart, name='cart'),
    path('add-to-cart/<int:pk>/', s_views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', s_views.remove_from_cart, name='remove_from_cart'),


]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
