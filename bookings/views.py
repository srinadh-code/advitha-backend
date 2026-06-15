
from room_management.models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer


class BookingAPIView(APIView):

    def get(self, request):

        bookings = Booking.objects.all()

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        room_id = request.data.get("room")

        try:
            room = Room.objects.get(id=room_id)

        except Room.DoesNotExist:

            return Response(
                {"message": "Room not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check room availability
        if room.available_rooms <= 0:

            return Response(
                {"message": "No Rooms Available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            booking = serializer.save()

            # Reduce available rooms
            room.available_rooms -= 1

            # Update availability flag
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking


class CancelBookingAPIView(APIView):

    def delete(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:

            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        room = booking.room

        room.available_rooms += 1

        if room.available_rooms > 0:
            room.is_available = True

        room.save()

        booking.delete()

        return Response(
            {"message": "Booking cancelled successfully"},
            status=status.HTTP_200_OK
        )
        
        
        
from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class TodayCheckInAPIView(APIView):

    def get(self, request):

        today = date.today()

        bookings = Booking.objects.filter(
            check_in=today,
            status="booked"
        )

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking


class CheckInBookingAPIView(APIView):

    def put(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:

            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        booking.status = "checked_in"
        booking.save()

        return Response({
            "message": "Guest checked in successfully"
        })    
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class TodayCheckOutAPIView(APIView):

    def get(self, request):

        today = date.today()

        bookings = Booking.objects.filter(
            check_out=today,
            status="checked_in"
        )

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking


class CheckOutBookingAPIView(APIView):

    def put(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        booking.status = "checked_out"
        booking.save()

        return Response({
            "message": "Guest checked out successfully"
        })
from room_management.models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer


class BookingAPIView(APIView):

    def get(self, request):

        bookings = Booking.objects.all()

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        room_id = request.data.get("room")

        try:
            room = Room.objects.get(id=room_id)

        except Room.DoesNotExist:

            return Response(
                {"message": "Room not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check room availability
        if room.available_rooms <= 0:

            return Response(
                {"message": "No Rooms Available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            booking = serializer.save()

            # Reduce available rooms
            room.available_rooms -= 1

            # Update availability flag
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


class CancelBookingAPIView(APIView):

    def delete(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:

            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        room = booking.room

        room.available_rooms += 1

        if room.available_rooms > 0:
            room.is_available = True

        room.save()

        booking.delete()

        return Response(
            {"message": "Booking cancelled successfully"},
            status=status.HTTP_200_OK
        )



class CheckInAPIView(APIView):

    def patch(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        booking.status = "checked_in"
        booking.save()

        return Response(
            {
                "message": "Guest checked in successfully",
                "status": booking.status
            },
            status=status.HTTP_200_OK
        )


class CheckOutAPIView(APIView):

    def patch(self, request, pk):

        try:
            booking = Booking.objects.get(pk=pk)

        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        booking.status = "checked_out"
        booking.save()

        return Response(
            {
                "message": "Guest checked out successfully",
                "status": booking.status
            },
            status=status.HTTP_200_OK
        )