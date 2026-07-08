


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
                if not serializer.is_valid():
                    print("Request Data:", request.data)
                    print("Validated Data:", serializer.validated_data)
                    print("Phone:", serializer.validated_data.get("phone"))
                    return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                    )
                if not request.user.phone_number:
                    request.user.phone_number = serializer.validated_data["phone"]
                    request.user.save()

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
    
    
    
    
    


from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking


from accounts.models import User

from events.models import EventBooking


from django.db.models import Q

class CustomerListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        customers = User.objects.filter(
            role="customer"
            ).filter(
             Q(bookings__isnull=False) |
             Q(event_bookings__isnull=False)
        ).distinct().order_by("username")
    
        data = []

        for customer in customers:

            room_count = Booking.objects.filter(
                user=customer
            ).count()

            event_count = EventBooking.objects.filter(
    user=customer,
    status="confirmed"
).count()
            latest_booking = (
                Booking.objects
                .filter(user=customer)
                .order_by("-created_at")
                .first()
            )

            data.append({
    "id": customer.id,
    "name": latest_booking.full_name if latest_booking else customer.username,
    "email": customer.email,
    "phone": customer.phone_number,
    "room_bookings_count": room_count,
    "event_bookings_count": event_count,
})

        return Response(data)
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Booking
from .serializers import CustomerBookingSerializer
from events.models import EventBooking
from events.serializers import CustomerEventBookingSerializer
from rest_framework.permissions import IsAuthenticated

class CustomerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
      

        room_bookings = (
            Booking.objects
            .filter(user_id=pk)
            .select_related("room")
            .order_by("-check_in")
        )

        event_bookings = (
    EventBooking.objects
    .filter(
        user_id=pk,
        status="confirmed"
    )
    .select_related("category")
    .order_by("-event_date")
)

        if not room_bookings.exists() and not event_bookings.exists():
            return Response(
                {"message": "Customer not found"},
                status=404
            )

        customer = User.objects.get(id=pk)

        data = {
            "id": customer.id,
            "name": customer.username,
            "email": customer.email,
            "phone": customer.phone_number,

            "room_bookings_count": room_bookings.count(),
            "event_bookings_count": event_bookings.count(),

            "room_bookings": CustomerBookingSerializer(
                room_bookings,
                many=True
            ).data,

            "event_bookings": CustomerEventBookingSerializer(
                event_bookings,
                many=True
            ).data,
        }

        return Response(data)