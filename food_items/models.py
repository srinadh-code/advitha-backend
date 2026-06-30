from django.db import models
from cloudinary.models import CloudinaryField

class FoodCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
class Food(models.Model):

    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.CASCADE,
        related_name="foods"
    )

    price = models.DecimalField( max_digits=10, decimal_places=2)

    image = CloudinaryField("image",blank=True,null=True)

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name