from django.contrib import admin
from .models import ServiceProvider

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'location', 'rating', 'price')
    list_filter = ('service_type', 'location')
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'image', 'short_desc')
        }),
        ('Service Details', {
            'fields': ('service_type', 'location', 'experience', 'event_types')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'rating', 'available_dates')
        }),
    )

admin.site.register(ServiceProvider, ServiceProviderAdmin)
