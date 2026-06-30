from django.urls import path

from .views import (
    FoodCategoryListView,
    FoodListCreateView,
    FoodDetailView
)

urlpatterns = [
    path(
        "categories/",
        FoodCategoryListView.as_view()
    ),

    path(
        "foods/",
        FoodListCreateView.as_view()
    ),

    path(
        "foods/<int:pk>/",
        FoodDetailView.as_view()
    ),
]