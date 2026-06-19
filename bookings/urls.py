




# from django.urls import path
# from .views import (
#     BookingAPIView,
#     CancelBookingAPIView,TodayCheckInAPIView,CheckInBookingAPIView,
#     TodayCheckOutAPIView,CheckOutBookingAPIView,CheckInAPIView,CheckOutAPIView
# )

# urlpatterns = [
#     path("",BookingAPIView.as_view(),name="bookings" ),

#     path(
#         "cancel/<int:pk>/",
#         CancelBookingAPIView.as_view(),
#         name="cancel-booking"
#     ),
#     path(
#            "check-in/",
#         TodayCheckInAPIView.as_view(),
#         name="today-checkin"
#     ),
#     path(
#     "check-in/<int:pk>/",
#     CheckInBookingAPIView.as_view(),
#     name="check-in-booking"
# ),
# path(
#     "check-out/",
#     TodayCheckOutAPIView.as_view(),
#     name="today-checkout"
# ),

# path(
#     "check-out/<int:pk>/",
#     CheckOutBookingAPIView.as_view(),
#     name="checkout-booking"
# ),
#     path(
#         "",
#         BookingAPIView.as_view(),
#         name="bookings"
#     ),

#     path(
#         "cancel/<int:pk>/",
#         CancelBookingAPIView.as_view(),
#         name="cancel-booking"
#     ),
#     path("checkin/<int:pk>/", CheckInAPIView.as_view()),
#     path("checkout/<int:pk>/", CheckOutAPIView.as_view()),

    
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
        name="today-checkin"
    ),

    path(
        "check-out/",
        TodayCheckOutAPIView.as_view(),
        name="today-checkout"
    ),

    path(
        "checkin/<int:pk>/",
        CheckInAPIView.as_view(),
        name="checkin"
    ),

    path(
        "checkout/<int:pk>/",
        CheckOutAPIView.as_view(),
        name="checkout"
    ),
]