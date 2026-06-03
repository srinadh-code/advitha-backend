from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TourismPlace
from .serializers import TourismPlaceSerializer


class TourismPlaceListAPIView(APIView):

    def get(self, request):

        places = TourismPlace.objects.all()

        serializer = TourismPlaceSerializer(
            places,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)