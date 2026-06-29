
from django.db import models
from django.conf import settings


class Booking(models.Model):

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="bookings",
    null=True,
    blank=True
)

    full_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    room = models.ForeignKey(
        "room_management.Room",
        on_delete=models.CASCADE
    )

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("booked", "Booked"),
            ("checked_in", "Checked In"),
            ("checked_out", "Checked Out"),
            ("cancelled", "Cancelled"),
        ],
        default="booked"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name