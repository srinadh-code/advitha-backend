from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EventCategory
from .serializers import (
    EventCategorySerializer
)
from .models import EventBooking
from .serializers import EventBookingSerializer
from rest_framework import status

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

    def get(self, request):

        bookings = EventBooking.objects.all().order_by("-created_at")

        serializer = EventBookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        event_date = request.data.get("event_date")

        already_booked = EventBooking.objects.filter(
            event_date=event_date
        ).exists()

        if already_booked:
            return Response(
                {
                    "error": f"Sorry, event hall is already booked for {event_date}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EventBookingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(status="confirmed")
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)