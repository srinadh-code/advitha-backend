
    
from django.db import models
from cloudinary.models import CloudinaryField
class Room(models.Model):

    ROOM_TYPES = [
        ('DELUXE', 'Deluxe'),
        ('PREMIUM', 'Premium'),
        ('SUITE', 'Suite'),
        ('EXECUTIVE', 'Executive'),
    ]

    title = models.CharField(max_length=100)
    total_rooms = models.IntegerField(default=1)

    available_rooms = models.IntegerField(default=1)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)

    image = CloudinaryField(
    "image",
    blank=True,
    null=True
)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    adults = models.IntegerField()
    children = models.IntegerField(default=0)

    feature1 = models.CharField(max_length=100)
    feature2 = models.CharField(max_length=100)
    feature3 = models.CharField(max_length=100)
    feature4 = models.CharField(max_length=100)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title