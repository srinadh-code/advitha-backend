from django.db import models
from django.db.models import Q, F
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
    features = models.JSONField(default=list, blank=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(available_rooms__lte=F("total_rooms")),
                name="available_lte_total",
            )
        ]

    def __str__(self):
        return self.title