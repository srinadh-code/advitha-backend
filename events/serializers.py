# from rest_framework import serializers
# from .models import EventCategory, EventBooking


# class EventCategorySerializer(
#     serializers.ModelSerializer
# ):
#     class Meta:
#         model = EventCategory
#         fields = "__all__"


# class EventBookingSerializer(
#     serializers.ModelSerializer
# ):
#     class Meta:
#         model = EventBooking
#         fields = "__all__"
        

from rest_framework import serializers
from .models import EventCategory, EventBooking


class EventCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EventCategory
        fields = [
            "id",
            "title",
            "image_url",
            "starting_price",
            "description",
            "is_active",
            "created_at",
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = "__all__"