




# class TourismPlaceListCreateAPIView(
#     generics.ListCreateAPIView
# ):
#     queryset = TourismPlace.objects.all()
#     serializer_class = TourismPlaceSerializer

#     def get_serializer_context(self):
#         return {
#             "request": self.request
#         }


# class TourismPlaceDetailAPIView(
#     generics.RetrieveUpdateDestroyAPIView
# ):
#     queryset = TourismPlace.objects.all()
#     serializer_class = TourismPlaceSerializer

#     def get_serializer_context(self):
#         return {
#             "request": self.request
#         }

# class HotelLocationView(APIView):
#     def get(self, request):
#         location = HotelLocation.objects.first()
#         serializer = HotelLocationSerializer(location)
#         return Response(serializer.data)



from .models import TourismPlace,HotelLocation
from .serializers import TourismPlaceSerializer,HotelLocationSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)




class TourismPlaceListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        places = TourismPlace.objects.all()

        serializer = TourismPlaceSerializer(
            places,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can add tourism places"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TourismPlaceSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



from django.shortcuts import get_object_or_404


class TourismPlaceDetailAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        return get_object_or_404(
            TourismPlace,
            id=pk
        )

    def get(self, request, pk):
        place = self.get_object(pk)

        serializer = TourismPlaceSerializer(
            place,
            context={"request": request}
        )

        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can update tourism places"},
                status=status.HTTP_403_FORBIDDEN
            )

        place = self.get_object(pk)

        serializer = TourismPlaceSerializer(
            place,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can update tourism places"},
                status=status.HTTP_403_FORBIDDEN
            )

        place = self.get_object(pk)

        serializer = TourismPlaceSerializer(
            place,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can delete tourism places"},
                status=status.HTTP_403_FORBIDDEN
            )

        place = self.get_object(pk)
        place.delete()

        return Response(
            {"message": "Deleted successfully"}
        )
        




class HotelLocationView(APIView):
    def get(self, request):
        location = HotelLocation.objects.first()

        if not location:
            return Response(
                {"error": "Hotel location not configured"},
                status=404
            )

        serializer = HotelLocationSerializer(location)
        return Response(serializer.data)