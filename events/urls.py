from django.urls import path
from .views import EventCategoryAPIView,EventBookingAPIView

urlpatterns = [
    path(
        "categories/",
        EventCategoryAPIView.as_view()
    ),
    # events/urls.py

path(
    "bookings/",
    EventBookingAPIView.as_view()
),
path(
    "bookings/<int:booking_id>/",
    EventBookingAPIView.as_view()
)
]