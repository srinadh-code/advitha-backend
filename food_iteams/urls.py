from django.urls import path
from .views import (
    FoodListCreateView,
    FoodDetailView
)

urlpatterns = [

    path(
        "foods/",
        FoodListCreateView.as_view(),
        name="food-list"
    ),

    path(
        "foods/<int:pk>/",
        FoodDetailView.as_view(),
        name="food-detail"
    ),
]