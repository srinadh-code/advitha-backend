from django.db import models


class TourismPlace(models.Model):

    CATEGORY_CHOICES = [
        ("Temples", "Temples"),
        ("Waterfalls", "Waterfalls"),
        ("Historical Places", "Historical Places"),
        ("Parks", "Parks"),
        ("Adventure Spots", "Adventure Spots"),
        ("View Points", "View Points"),
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    image = models.ImageField(
    upload_to="tourism/"
)

    distance = models.CharField(max_length=50)

    hours = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name