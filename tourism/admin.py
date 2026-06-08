from django.contrib import admin

from .models import TourismPlace


@admin.register(TourismPlace)
class TourismPlaceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "distance",
        "hours",
    )

    search_fields = (
        "name",
        "category",
    )

    list_filter = (
        "category",
    )