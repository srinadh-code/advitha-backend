from django.urls import path
from .views import ContactUsView,ReceptionistContactAPIView

urlpatterns = [
    path("", ContactUsView.as_view(), name="contact"),
    path(
        "receptionist/",
        ReceptionistContactAPIView.as_view(),
        name="receptionist-contact",
    ),
]