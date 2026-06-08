# from rest_framework.views import APIView
# from rest_framework.response import Response

# from .models import GalleryImage
# from .serializers import GalleryImageSerializer


# class GalleryListAPIView(APIView):

#     def get(self, request):

#         images = GalleryImage.objects.all().order_by("-created_at")

#         serializer = GalleryImageSerializer(
#             images,
#             many=True
#         )

#         return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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


class GalleryCreateAPIView(APIView):

    def post(self, request):

        serializer = GalleryImageSerializer(
            data=request.data
        )

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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import GalleryImage
from .serializers import GalleryImageSerializer


class GalleryDetailAPIView(APIView):

    def get_object(self, pk):
        return GalleryImage.objects.get(id=pk)

    def get(self, request, pk):

        image = self.get_object(pk)

        serializer = GalleryImageSerializer(image)

        return Response(serializer.data)

    def put(self, request, pk):

        image = self.get_object(pk)

        serializer = GalleryImageSerializer(
            image,
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

    def patch(self, request, pk):

        image = self.get_object(pk)

        serializer = GalleryImageSerializer(
            image,
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

        image = self.get_object(pk)

        image.delete()

        return Response(
            {"message": "Deleted Successfully"}
        )