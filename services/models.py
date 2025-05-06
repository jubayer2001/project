from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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

    event_types = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='wedding'
    )

    available_dates = models.JSONField(default=list)  # For date filtering

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    location = models.CharField(max_length=20, choices=LOCATIONS)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.IntegerField()
    experience = models.PositiveIntegerField()
    short_desc = models.TextField()
    image = models.ImageField(upload_to='service_providers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"