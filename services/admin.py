from django.contrib import admin
from .models import ServiceProvider, Service, PackageFeature, Event

# Admin configuration for Service
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Service, ServiceAdmin)

# Admin configuration for PackageFeature
class PackageFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(PackageFeature, PackageFeatureAdmin)

# Admin configuration for ServiceProvider
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'location', 'rating', 'price', 'is_verified')
    list_filter = ('service_type', 'location', 'is_verified')
    search_fields = ('name',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'image', 'short_desc', 'is_verified')
        }),
        ('Service Details', {
            'fields': ('service_type', 'location', 'experience', 'event_types', 'events_completed', 'languages', 'travel_info')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'price_unit', 'rating', 'available_dates')
        }),
        ('Relationships', {
            'fields': ('services_offered', 'package_features')
        }),
    )
    filter_horizontal = ('services_offered', 'package_features')

# Register the ServiceProvider model in the admin panel
admin.site.register(ServiceProvider, ServiceProviderAdmin)

# Admin configuration for Event
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'event_date', 'date_created', 'user')
    list_filter = ('event_date', 'location', 'user')
    search_fields = ('name', 'location', 'user__username')
    date_hierarchy = 'event_date'
    ordering = ('-date_created',)  # Orders events by the most recent created date

    filter_horizontal = ('services',)

# Register the Event model in the admin panel
admin.site.register(Event, EventAdmin)
