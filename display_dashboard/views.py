
from rest_framework.views import APIView
from rest_framework.response import Response
from bookings.models import Booking
from room_management.models import Room
from accounts.models import User
from events.models import EventBooking
from room_management.models import Room


class DashboardAPIView(APIView):
    def get(self, request):
        total_bookings = Booking.objects.count()
        total_rooms = sum(room.total_rooms for room in Room.objects.all())
        available_rooms = sum(
        room.available_rooms for room in Room.objects.all())

        total_rooms = sum(room.total_rooms for room in Room.objects.all())

        occupied_rooms = total_rooms - available_rooms
        occupancy_rate = 0
        if total_rooms > 0:
            occupancy_rate = round(
                (occupied_rooms / total_rooms) * 100,
                2
            )
        total_customers = User.objects.filter(role="customer").count()

        bookings = Booking.objects.order_by("-created_at")[:5]
        total_staff = User.objects.filter(role="staff").count()
        total_receptionists = User.objects.filter(role="receptionist").count()
        total_event_bookings = EventBooking.objects.count()
        recent_event_bookings = EventBooking.objects.order_by("-id")[:5]
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
        })