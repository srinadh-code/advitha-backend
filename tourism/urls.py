


from django.urls import path

from .views import (
    TourismPlaceListCreateAPIView,
    TourismPlaceDetailAPIView,HotelLocationView
    
)

urlpatterns = [

    path(
        "places/",
        TourismPlaceListCreateAPIView.as_view(),
        name="tourism-list-create"
    ),

    path(
        "places/<int:pk>/",
        TourismPlaceDetailAPIView.as_view(),
        name="tourism-detail"
    ),
    path("hotel-location/", HotelLocationView.as_view()),

]