from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "status",
        "created_at",
    )

    list_filter = ("status",)
    search_fields = ("name", "email", "phone")