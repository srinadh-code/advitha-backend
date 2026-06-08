# from django.urls import path
# from .views import BookingAPIView

# urlpatterns = [
#     path(
#         "",
#         BookingAPIView.as_view(),
#         name="bookings"
#     ),
# ]


from django.urls import path
from .views import (
    BookingAPIView,
    CancelBookingAPIView
)

urlpatterns = [
    path(
        "",
        BookingAPIView.as_view(),
        name="bookings"
    ),

    path(
        "cancel/<int:pk>/",
        CancelBookingAPIView.as_view(),
        name="cancel-booking"
    ),
]