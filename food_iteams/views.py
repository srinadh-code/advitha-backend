from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Food
from .serializers import FoodSerializer





class FoodListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        print("DATA:", request.data)
        print("FILES:", request.FILES)

        serializer = self.get_serializer(data=request.data)

        print(serializer.is_valid())
        print(serializer.errors)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data)
    def get_queryset(self):
        category=self.request.GET.get("category")
        if category:
            return Food.objects.filter(category=category)
        return Food.objects.all()

class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    parser_classes = [MultiPartParser, FormParser]