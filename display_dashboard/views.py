
from rest_framework.views import APIView
from rest_framework.response import Response
from bookings.models import Booking
from room_management.models import Room
from accounts.models import User
from events.models import EventBooking

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum
class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response(
                {"error": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        total_bookings = Booking.objects.count()
        # total_rooms = sum(room.total_rooms for room in Room.objects.all())
        # available_rooms = sum(
        # room.available_rooms for room in Room.objects.all())

        # total_rooms = sum(room.total_rooms for room in Room.objects.all())
        room_data = Room.objects.aggregate(
            total=Sum("total_rooms"),
            available=Sum("available_rooms")
        )

        total_rooms = room_data["total"] or 0
        available_rooms = room_data["available"] or 0

        occupied_rooms = total_rooms - available_rooms
        occupancy_rate = 0
        if total_rooms > 0:
            occupancy_rate = round(
                (occupied_rooms / total_rooms) * 100,
                2
            )
        total_customers = User.objects.filter(role="customer").count()
        today_checkins = Booking.objects.filter(
        status="checked_in"
        ).count()

        today_checkouts = Booking.objects.filter(
        status="checked_out"
        ).count()

        active_bookings = Booking.objects.filter(
        status="booked"
        ).count()
        bookings = Booking.objects.order_by("-created_at")[:5]
        total_staff = User.objects.filter(role="staff").count()
        total_receptionists = User.objects.filter(role="receptionist").count()
        total_event_bookings = EventBooking.objects.count()
        recent_event_bookings = EventBooking.objects.order_by("-created_at")[:5]
        
        event_booking_data = [
            {
                "name": booking.name,
                "event_type": booking.category.title,
                "event_date": booking.event_date,
                "guests": booking.guests,
            }
            for booking in recent_event_bookings
        ]

        recent_bookings = [
            {
                "guest": booking.full_name,
                "room": str(booking.room),
                "check_in": booking.check_in,
                "status": booking.status,
            }
            for booking in bookings
        ]

        return Response({
            "total_bookings": total_bookings,
            "available_rooms": available_rooms,
            "occupied_rooms": occupied_rooms,
            "restaurant_reservations": 0,
            "total_customers": total_customers,
            "recent_bookings": recent_bookings,
            "total_staff": total_staff,
            "total_receptionists": total_receptionists,
            "total_event_bookings": total_event_bookings,
            "recent_event_bookings": event_booking_data,
            "occupancy_rate": occupancy_rate,
            "total_rooms": total_rooms,
            "today_checkins": today_checkins,
            "today_checkouts": today_checkouts,
            "active_bookings": active_bookings,
        })