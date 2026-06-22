


from django.urls import path
from .views import (
    ContactUsView,
    ReceptionistContactAPIView,
    ReceptionistEnquiriesAPIView,
    ReplyContactAPIView
)

urlpatterns = [
    path("", ContactUsView.as_view()),

    path(
        "receptionist/",
        ReceptionistContactAPIView.as_view()
    ),

    path(
        "enquiries/",
        ReceptionistEnquiriesAPIView.as_view()
    ),

    path(
        "reply/<int:enquiry_id>/",
        ReplyContactAPIView.as_view()
    ),
]