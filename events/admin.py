from django.contrib import admin
from .models import EventCategory, EventBooking


admin.site.register(EventCategory)
admin.site.register(EventBooking)