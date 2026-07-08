from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class EventCategory(models.Model):

    title = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending"
    )

    image = CloudinaryField(
        blank=True,
        max_length=255,
        null=True,
        verbose_name="image",
    )

    starting_price = models.PositiveIntegerField()

    description = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
    
    


class EventBooking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_bookings",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        EventCategory,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    event_date = models.DateField()

    guests = models.PositiveIntegerField()

    special_request = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name