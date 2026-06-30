from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Food, FoodCategory
from .serializers import (
    FoodSerializer,
    FoodCategorySerializer
)


class FoodCategoryListView(generics.ListAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer


class FoodListCreateView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    parser_classes = [MultiPartParser, FormParser]


class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    parser_classes = [MultiPartParser, FormParser]