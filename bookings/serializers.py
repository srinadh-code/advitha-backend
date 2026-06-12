from rest_framework import serializers
from .models import  Booking



class BookingSerializer(serializers.ModelSerializer):

    room_name = serializers.CharField(
        source="room.title",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "room",
            "room_name",
            "check_in",
            "check_out",
            "guests",
            "status",
            "created_at",
        ]