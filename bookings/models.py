from django.db import models
# from rooms.models import Room

class Booking(models.Model):

    full_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    room = models.ForeignKey(
        'room_management.Room',
        on_delete=models.CASCADE
    )

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name