from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ServiceProvider
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404

@login_required
def services(request):
    # Get available choices from model
    service_types = ServiceProvider.SERVICE_TYPES
    locations = ServiceProvider.LOCATIONS
    event_types = ServiceProvider.EVENT_TYPES

    context = {
        'service_types': service_types,
        'locations': locations,
        'event_types': event_types
    }
    return render(request, 'services/services.html', context)


@login_required
def search_results(request):
    service_type = request.GET.get('serviceType')
    location = request.GET.get('location')
    event_type = request.GET.get('eventType')
    event_date = request.GET.get('eventDate')

    filters = Q()

    if service_type:
        filters &= Q(service_type=service_type)
    if location:
        filters &= Q(location=location)
    if event_type:
        filters &= Q(event_types=event_type)
    if event_date:
        filters &= Q(available_dates__icontains=event_date)

    providers = ServiceProvider.objects.filter(filters).order_by('-rating')

    context = {
        'providers': providers,
        'service_type': service_type,
        'location': location,
        'event_type': event_type,
        'event_date': event_date
    }
    return render(request, 'services/search_results.html', context)


@login_required
def provider_detail(request, pk):
    provider = get_object_or_404(ServiceProvider, pk=pk)
    return render(request, 'services/provider-details.html', {'provider': provider})
@login_required
def cart(request):
    cart = request.session.get('cart', [])
    providers = ServiceProvider.objects.filter(id__in=cart)
    total = sum([p.price for p in providers])  # Sum the prices directly as integers
    return render(request, 'services/cart.html', {'providers': providers, 'total': total})
@login_required
def add_to_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
    return redirect('cart')
@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
    return redirect('cart')