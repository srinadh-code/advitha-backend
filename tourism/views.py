


from rest_framework import generics
from rest_framework.views import APIView
from .models import TourismPlace,HotelLocation
from .serializers import TourismPlaceSerializer


class TourismPlaceListCreateAPIView(
    generics.ListCreateAPIView
):
    queryset = TourismPlace.objects.all()
    serializer_class = TourismPlaceSerializer

    def get_serializer_context(self):
        return {
            "request": self.request
        }


class TourismPlaceDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = TourismPlace.objects.all()
    serializer_class = TourismPlaceSerializer

    def get_serializer_context(self):
        return {
            "request": self.request
        }
        


class HotelLocationView(APIView):
    def get(self, request):
        location = HotelLocation.objects.first()
        serializer = HotelLocationSerializer(location)
        return Response(serializer.data)