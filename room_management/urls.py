from django.urls import path
from .views import RoomAPIView

urlpatterns = [
    path(
        "",
        RoomAPIView.as_view()
    ),

    path(
        "<int:pk>/",
        RoomAPIView.as_view()
    ),
]