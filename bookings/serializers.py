
from datetime import date
from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    room_name = serializers.CharField(
        source="room.title",
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
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

        read_only_fields = [
            "user",
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")

        if check_in < date.today():
            raise serializers.ValidationError({
                "check_in": "Check-in date cannot be in the past."
            })

        if check_out <= check_in:
            raise serializers.ValidationError({
                "check_out": "Check-out date must be after check-in date."
            })

        return attrs
    
from rest_framework import serializers
from .models import Booking


class CustomerBookingSerializer(serializers.ModelSerializer):
    room = serializers.CharField(source="room.title")

    class Meta:
        model = Booking
        fields = [
            "id",
            "room",
            "check_in",
            "check_out",
            "guests",
            "status",
        ]