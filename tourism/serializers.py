

from rest_framework import serializers
from .models import TourismPlace


class TourismPlaceSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TourismPlace
        fields = "__all__"

    def get_image_url(self, obj):

        request = self.context.get("request")

        if obj.image:
            return request.build_absolute_uri(
                obj.image.url
            )

        return None
    


from rest_framework import serializers
from .models import HotelLocation

class HotelLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLocation
        fields = "__all__"