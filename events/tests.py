from django.test import TestCase

from .models import EventCategory
from .serializers import EventCategorySerializer


class EventCategorySerializerTests(TestCase):
    def test_serializer_returns_category_data_without_image(self):
        category = EventCategory.objects.create(
            title="Birthday Party",
            starting_price=5000,
            description="Perfect for birthday celebrations",
            is_active=True,
        )

        serializer = EventCategorySerializer(category)

        self.assertEqual(serializer.data["title"], "Birthday Party")
        self.assertEqual(serializer.data["starting_price"], 5000)
        self.assertIsNone(serializer.data["image_url"])
