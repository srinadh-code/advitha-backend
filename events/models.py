from django.db import models

from cloudinary.models import CloudinaryField

class EventCategory(models.Model):

    title = models.CharField(max_length=100)

    image = CloudinaryField(
    "image",
    blank=True,
    null=True
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
    
    
    
from django.db import models


class EventBooking(models.Model):

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