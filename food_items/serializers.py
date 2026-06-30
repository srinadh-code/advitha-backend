



from rest_framework import serializers
from .models import Food, FoodCategory


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = "__all__"

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.build_url(
                width=800,
                crop="scale",
                quality="auto",
                fetch_format="auto"
            )
        return None