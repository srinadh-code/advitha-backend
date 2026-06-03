from django.contrib import admin
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "created_at",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "title",
    )