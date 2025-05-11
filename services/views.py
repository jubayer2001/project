from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ServiceProvider,Event
from django.db.models import Q
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg


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
        request.session['event_date'] = event_date  #  save date in session

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

from datetime import datetime

@login_required
def create_event(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_location = request.POST.get('event_location')
        service_ids = request.session.get('cart', [])

        # Check if cart is empty
        if not service_ids:
            messages.error(request, "Your cart is empty. Please add services before creating an event.")
            return redirect('cart')

        #  Get event date from session
        event_date_str = request.session.get('event_date')
        if not event_date_str:
            messages.error(request, "Event date is missing. Please search for services again and set the date.")
            return redirect('cart')

        #  Convert to datetime
        try:
            # If the date comes as 'YYYY-MM-DD' from search input, convert it properly
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        except ValueError:
            messages.error(request, "Invalid event date format in session.")
            return redirect('cart')

        # Create the Event
        event = Event.objects.create(
            user=request.user,
            name=event_name,
            location=event_location,
            event_date=event_date  #  save date from session
        )

        # Assign the selected service providers to the event
        providers = ServiceProvider.objects.filter(id__in=service_ids)
        event.services.set(providers)

        # Clear the cart after creating the event
        request.session['cart'] = []
        request.session['event_date'] = None  #  clear the date after use

        messages.success(request, f"Event '{event.name}' created successfully with {providers.count()} services!")

        return redirect('events')

    # If not POST, fallback redirect to cart
    return redirect('cart')


from django.utils import timezone

from django.db.models import Avg
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Event, ServiceProvider

from django.db.models import Avg
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Event, ServiceProvider

@login_required
def events_page(request):
    user = request.user
    events = Event.objects.filter(user=user).distinct()

    # Filtering by event_type from the related ServiceProvider's event_types
    event_type = request.GET.get('event_type')
    if event_type:
        events = events.filter(services__event_types=event_type).distinct()

    # Sorting by selected criteria
    sort_by = request.GET.get('sort_by')
    if sort_by == 'date':
        events = events.order_by('event_date')
    elif sort_by == 'rating':
        events = events.annotate(avg_rating=Avg('services__rating')).order_by('-avg_rating')

    # Count total events and upcoming events
    total_events = events.count()
    upcoming_events = events.filter(event_date__gte=timezone.now()).count()
    avg_rating = events.aggregate(Avg('services__rating'))['services__rating__avg']

    context = {
        'events': events,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'selected_event_type': event_type,
        'selected_sort_by': sort_by,
    }
    return render(request, 'services/events.html', context)

