from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EventCategory
from .serializers import (
    EventCategorySerializer
)
from .models import EventBooking
from .serializers import EventBookingSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class EventCategoryAPIView(APIView):

    def get(self, request):

        categories = EventCategory.objects.filter(
            is_active=True
        )

        serializer = EventCategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)
    



class EventBookingAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Logged in user:", request.user.id, request.user.email)
        if request.user.role not in ["admin", "receptionist"]:
            return Response(
                {"error": "You are not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )

        bookings = EventBooking.objects.all().order_by("-created_at")
        serializer = EventBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventBookingSerializer(data=request.data)

        if serializer.is_valid():
            event_date = serializer.validated_data["event_date"]

            already_booked = EventBooking.objects.filter(
                event_date=event_date
            ).exists()

            if already_booked:
                return Response(
                    {
                        "error": (
                f"Sorry, event hall is already booked for {event_date}. "
                "Please select another date."
            )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    def patch(self, request, booking_id):
        if request.user.role not in ["admin", "receptionist"]:
            return Response(
                {"error": "Not authorized"},
                status=403
            )

        try:
            booking = EventBooking.objects.get(id=booking_id)
        except EventBooking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        booking.status = "confirmed"
        booking.save()

        return Response({"message": "Booking confirmed"})