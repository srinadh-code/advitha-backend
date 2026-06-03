from django.urls import path
from .views import TourismPlaceListAPIView

urlpatterns = [
    path(
        "places/",
        TourismPlaceListAPIView.as_view()
    ),
]