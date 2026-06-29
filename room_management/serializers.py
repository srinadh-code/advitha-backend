# from rest_framework import serializers
# from .models import Room

# class RoomSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Room
#         fields = "__all__"




from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "id",
            "title",
            "total_rooms",
            "available_rooms",
            "room_type",
            "description",
            "price",
            "image",
            "image_url",
        ]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None