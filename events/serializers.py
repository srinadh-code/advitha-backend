

# from rest_framework import serializers
# from .models import EventCategory, EventBooking


# class EventCategorySerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = EventCategory
#         fields = [
#             "id",
#             "title",
#             "image_url",
#             "starting_price",
#             "description",
#             "is_active",
#             "created_at",
#         ]

#     def get_image_url(self, obj):
#         image_field = getattr(obj, "image", None)
#         if image_field:
#             return getattr(image_field, "url", None)
#         return None




# class EventBookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EventBooking
#         fields = [
#             "id",
#             "name",
#             "phone",
#             "event_date",
#             "guests",
#             "category",
#             "status",
#             "created_at",
#         ]

#         extra_kwargs = {
#             "status": {"read_only": True}
#         }

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
        image_field = getattr(obj, "image", None)
        if image_field:
            return getattr(image_field, "url", None)
        return None


class EventBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventBooking
        fields = [
            "id",
            "user",          # ← Add this
            "name",
            "phone",
            "event_date",
            "guests",
            "category",
            "status",
            "created_at",
        ]

        extra_kwargs = {
            "status": {"read_only": True},
            "user": {"read_only": True},   # ← User is set by backend
        }
        
class CustomerEventBookingSerializer(serializers.ModelSerializer):
    event = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = EventBooking
        fields = [
            "id",
            "event",
            "event_date",
            "guests",
            "status",
        ]