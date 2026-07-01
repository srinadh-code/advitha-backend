

    
from rest_framework import serializers
from .models import TourismPlace

from .models import HotelLocation


class TourismPlaceSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TourismPlace
        fields = "__all__"

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class HotelLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLocation
        fields = "__all__"