from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PackageFeature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    SERVICE_TYPES = (
        ('photographer', 'Photographer'),
        ('decorator', 'Decorator'),
        ('caterer', 'Caterer'),
    )

    LOCATIONS = (
        ('dhaka', 'Dhaka'),
        ('chattogram', 'Chattogram'),
        ('khulna', 'Khulna'),
        ('rajshahi', 'Rajshahi'),
        ('barishal', 'Barishal'),
        ('sylhet', 'Sylhet'),
        ('mymensingh', 'Mymensingh'),
        ('rangpur', 'Rangpur'),
    )

    EVENT_TYPES = (
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate Event'),
        ('anniversary', 'Anniversary'),
        ('party', 'Party'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='service_providers/')
    short_desc = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    location = models.CharField(max_length=20, choices=LOCATIONS)
    event_types = models.CharField(max_length=20, choices=EVENT_TYPES, default='wedding')
    available_dates = models.JSONField(default=list)
    experience = models.PositiveIntegerField()
    events_completed = models.PositiveIntegerField(default=0)  # NEW
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.IntegerField()
    price_unit = models.CharField(max_length=50, default='per event')  # NEW
    is_verified = models.BooleanField(default=False)  # NEW
    languages = models.CharField(max_length=200, default='Bangla, English')  # NEW
    travel_info = models.CharField(max_length=200, default='Within city')  # NEW

    services_offered = models.ManyToManyField(Service, blank=True, related_name='providers')  # NEW
    package_features = models.ManyToManyField(PackageFeature, blank=True, related_name='providers')  # NEW

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"



class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    services = models.ManyToManyField('ServiceProvider')  # Assuming Provider is your service provider model

    def __str__(self):
        return f"{self.name} at {self.location}"
