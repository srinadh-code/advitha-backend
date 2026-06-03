from django.db import models
from cloudinary.models import CloudinaryField


class Food(models.Model):

    CATEGORY_CHOICES = [
        ("Veg", "Veg"),
        ("Non Veg", "Non Veg"),
        ("Starters", "Starters"),
        ("Drinks", "Drinks"),
        ("Ice Creams", "Ice Creams"),
        ("Restaurant Specials", "Restaurant Specials"),
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name