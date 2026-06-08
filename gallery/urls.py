from django.urls import path

from .views import (
    GalleryListAPIView,
    GalleryCreateAPIView,
    GalleryDetailAPIView,
)

urlpatterns = [

    path(
        "images/",
        GalleryListAPIView.as_view()
    ),

    path(
        "images/create/",
        GalleryCreateAPIView.as_view()
    ),

    path(
        "images/<int:pk>/",
        GalleryDetailAPIView.as_view()
    ),
]