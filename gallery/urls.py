from django.urls import path
from .views import GalleryListAPIView

urlpatterns = [
    path(
        "images/",
        GalleryListAPIView.as_view()
    ),
]