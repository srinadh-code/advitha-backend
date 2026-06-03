from django.db import models
from cloudinary.models import CloudinaryField


class GalleryImage(models.Model):

    CATEGORY_CHOICES = [
        ("Hotel", "Hotel"),
        ("Rooms", "Rooms"),
        ("Restaurant", "Restaurant"),
        ("Tourism", "Tourism"),
        ("Customer Experiences", "Customer Experiences"),
    ]

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    image = CloudinaryField(
        "image"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title