from rest_framework.views import APIView
from rest_framework.response import Response

from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryListAPIView(APIView):

    def get(self, request):

        images = GalleryImage.objects.all().order_by("-created_at")

        serializer = GalleryImageSerializer(
            images,
            many=True
        )

        return Response(serializer.data)