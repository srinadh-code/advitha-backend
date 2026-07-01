
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Room
# from .serializers import RoomSerializer


# class RoomAPIView(APIView):

#     def get(self, request):
#         rooms = Room.objects.all()

#         serializer = RoomSerializer(
#             rooms,
#             many=True
#         )

#         return Response(serializer.data)

#     def post(self, request):
#         serializer = RoomSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def patch(self, request, pk):
#         room = Room.objects.get(pk=pk)

#         serializer = RoomSerializer(
#             room,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, pk):
#         room = Room.objects.get(pk=pk)

#         room.delete()

#         return Response(
#             {"message": "Room deleted"},
#             status=status.HTTP_204_NO_CONTENT
#         )

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Room
from .serializers import RoomSerializer


class RoomAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        rooms = Room.objects.all()

        serializer = RoomSerializer(
            rooms,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can create rooms."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RoomSerializer(data=request.data)

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

    def patch(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can update rooms."},
                status=status.HTTP_403_FORBIDDEN
            )

        room = get_object_or_404(Room, pk=pk)

        serializer = RoomSerializer(
            room,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can delete rooms."},
                status=status.HTTP_403_FORBIDDEN
            )

        room = get_object_or_404(Room, pk=pk)

        room.delete()

        return Response(
            {"message": "Room deleted"},
            status=status.HTTP_200_OK
        )