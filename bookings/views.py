
# from datetime import date
# from room_management.models import Room
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Booking
# from .serializers import BookingSerializer


# class BookingAPIView(APIView):
#     def get(self, request):
#         bookings = Booking.objects.all()
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         room_id = request.data.get("room")

#         try:
#             room = Room.objects.get(id=room_id)
#         except Room.DoesNotExist:
#             return Response(
#                 {"message": "Room not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if room.available_rooms <= 0:
#             return Response(
#                 {"message": "No Rooms Available"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = BookingSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             room.available_rooms -= 1
#             if room.available_rooms == 0:
#                 room.is_available = False
#             room.save()

#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)


# class CancelBookingAPIView(APIView):
#     def delete(self, request, pk):
#         try:
#             booking = Booking.objects.get(pk=pk)
#         except Booking.DoesNotExist:
#             return Response({"message": "Booking not found"}, status=404)

#         room = booking.room
#         room.available_rooms += 1
#         room.is_available = True
#         room.save()

#         booking.delete()

#         return Response({"message": "Cancelled"})


# class TodayCheckInAPIView(APIView):
#     def get(self, request):
#         today = date.today()
#         bookings = Booking.objects.filter(
#             check_in=today,
#             status="booked"
#         )
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data)


# class TodayCheckOutAPIView(APIView):
#     def get(self, request):
#         today = date.today()
#         bookings = Booking.objects.filter(
#             check_out=today,
#             status="checked_in"
#         )
#         serializer = BookingSerializer(bookings, many=True)
#         return Response(serializer.data)


# class CheckInAPIView(APIView):
#     def patch(self, request, pk):
#         booking = Booking.objects.get(pk=pk)
#         booking.status = "checked_in"
#         booking.save()

#         return Response({"message": "Checked in"})
    



# class CheckOutAPIView(APIView):
#     def patch(self, request, pk):
#         try:
#             booking = Booking.objects.get(pk=pk)
#         except Booking.DoesNotExist:
#             return Response({"message": "Not found"}, status=404)

#         # STOP duplicate checkout
#         if booking.status == "checked_out":
#             return Response(
#                 {"message": "Already checked out"},
#                 status=400
#             )

#         room = booking.room

#         booking.status = "checked_out"
#         booking.save()

#         # increase safely
#         if room.available_rooms < room.total_rooms:
#             room.available_rooms += 1

#         room.save()

#         return Response({"message": "Checked out"})


from datetime import date
from room_management.models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from django.db import transaction
from .permissions import  IsAdminOrReceptionist
class BookingAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role in ["admin", "receptionist"]:
            bookings = Booking.objects.all()
        else:
            bookings = Booking.objects.filter(user=request.user)
        

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):

        room_id = request.data.get("room")

        try:
            with transaction.atomic():

                room = Room.objects.select_for_update().get(id=room_id)

                if room.available_rooms <= 0:
                    return Response(
                        {"message": "No Rooms Available"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                serializer = BookingSerializer(data=request.data)

                if serializer.is_valid():

                    serializer.save(user=request.user)

                    room.available_rooms -= 1

                    if room.available_rooms == 0:
                        room.is_available = False

                    room.save()

                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )

                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Room.DoesNotExist:
            return Response(
                {"message": "Room not found"},
                status=status.HTTP_404_NOT_FOUND
            )
class CancelBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            booking.user != request.user and
            request.user.role not in ["admin", "receptionist"]
        ):
            return Response(
                {"message": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        room = booking.room

        room.available_rooms = min(
            room.available_rooms + 1,
            room.total_rooms
        )

        room.is_available = room.available_rooms > 0
        room.save()

        booking.delete()

        return Response({"message": "Cancelled"})

class TodayCheckInAPIView(APIView):
    permission_classes = [IsAdminOrReceptionist]
    def get(self, request):
        today = date.today()
        bookings = Booking.objects.filter(
            check_in=today,
            status="booked"
        )
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class TodayCheckOutAPIView(APIView):
    permission_classes = [IsAdminOrReceptionist]
    def get(self, request):
        today = date.today()
        bookings = Booking.objects.filter(
            check_out=today,
            status="checked_in"
        )
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class CheckInAPIView(APIView):
    permission_classes = [IsAdminOrReceptionist]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if booking.status != "booked":
            return Response(
                {"message": "Cannot check in this booking"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = "checked_in"
        booking.save()

        return Response({"message": "Checked in"})



class CheckOutAPIView(APIView):
    permission_classes = [IsAdminOrReceptionist]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if booking.status != "checked_in":
            return Response(
                {"message": "Cannot check out this booking"},
                status=status.HTTP_400_BAD_REQUEST
            )

        room = booking.room

        booking.status = "checked_out"
        booking.save()

        if room.available_rooms < room.total_rooms:
            room.available_rooms += 1

        room.save()

        return Response({"message": "Checked out"})