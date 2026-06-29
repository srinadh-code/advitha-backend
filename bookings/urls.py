


# from django.urls import path
# from .views import (
#     BookingAPIView,
#     CancelBookingAPIView,
#     TodayCheckInAPIView,
#     TodayCheckOutAPIView,
#     CheckInAPIView,
#     CheckOutAPIView,
# )

# urlpatterns = [
#     path("", BookingAPIView.as_view(), name="bookings"),

#     path(
#         "cancel/<int:pk>/",
#         CancelBookingAPIView.as_view(),
#         name="cancel-booking"
#     ),

#     path(
#         "check-in/",
#         TodayCheckInAPIView.as_view(),
#         name="today-checkin"
#     ),

#     path(
#         "check-out/",
#         TodayCheckOutAPIView.as_view(),
#         name="today-checkout"
#     ),

#     path(
#         "checkin/<int:pk>/",
#         CheckInAPIView.as_view(),
#         name="checkin"
#     ),

#     path(
#         "checkout/<int:pk>/",
#         CheckOutAPIView.as_view(),
#         name="checkout"
#     ),
# ]



from django.urls import path
from .views import (
    BookingAPIView,
    CancelBookingAPIView,
    TodayCheckInAPIView,
    TodayCheckOutAPIView,
    CheckInAPIView,
    CheckOutAPIView,
)

urlpatterns = [
    path("", BookingAPIView.as_view(), name="bookings"),

    path(
        "cancel/<int:pk>/",
        CancelBookingAPIView.as_view(),
        name="cancel-booking"
    ),

    path(
        "check-in/",
        TodayCheckInAPIView.as_view(),
        name="today-check-in"
    ),

    path(
        "check-out/",
        TodayCheckOutAPIView.as_view(),
        name="today-check-out"
    ),

    path(
        "checkin/<int:pk>/",
        CheckInAPIView.as_view(),
        name="check-in"
    ),

    path(
        "checkout/<int:pk>/",
        CheckOutAPIView.as_view(),
        name="check-out"
    ),
    path(
    "my/",
    BookingAPIView.as_view(),
    name="my-bookings"
),
]