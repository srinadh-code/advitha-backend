from rest_framework import serializers
from .models import EventCategory, EventBooking


class EventCategorySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = EventCategory
        fields = "__all__"


class EventBookingSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = EventBooking
        fields = "__all__"
        

