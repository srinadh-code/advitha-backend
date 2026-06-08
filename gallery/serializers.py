from rest_framework import serializers
from .models import GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = [
            "id",
            "title",
            "category",
            "image",
            "image_url",
            "created_at",
        ]

    def get_image_url(self, obj):

        if obj.image:
            return obj.image.url

        return None