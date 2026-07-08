

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import GalleryImage
from .serializers import GalleryImageSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny


class GalleryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        images = GalleryImage.objects.all().order_by("-created_at")

        serializer = GalleryImageSerializer(
            images,
            many=True
        )

        return Response(serializer.data)

class GalleryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can upload gallery images"},
                status=status.HTTP_403_FORBIDDEN
            )

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
# class GalleryCreateAPIView(APIView):

#     def post(self, request):

#         serializer = GalleryImageSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )




# class GalleryDetailAPIView(APIView):

#     def get_object(self, pk):
#         return GalleryImage.objects.get(id=pk)

#     def get(self, request, pk):

#         image = self.get_object(pk)

#         serializer = GalleryImageSerializer(image)

#         return Response(serializer.data)

#     def put(self, request, pk):

#         image = self.get_object(pk)

#         serializer = GalleryImageSerializer(
#             image,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def patch(self, request, pk):

#         image = self.get_object(pk)

#         serializer = GalleryImageSerializer(
#             image,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     def delete(self, request, pk):

#         image = self.get_object(pk)

#         image.delete()

#         return Response(
#             {"message": "Deleted Successfully"}
#         )



class GalleryDetailAPIView(APIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return [IsAuthenticated()]

    def get_object(self, pk):
        return get_object_or_404(
            GalleryImage,
            id=pk
        )

    def get(self, request, pk):
        image = self.get_object(pk)
        serializer = GalleryImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can update gallery images"},
                status=status.HTTP_403_FORBIDDEN
            )

        image = self.get_object(pk)
        serializer = GalleryImageSerializer(
            image,
            data=request.data,
            
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can update gallery images"},
                status=status.HTTP_403_FORBIDDEN
            )

        image = self.get_object(pk)
        serializer = GalleryImageSerializer(
            image,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if request.user.role != "admin":
            return Response(
                {"error": "Only admin can delete gallery images"},
                status=status.HTTP_403_FORBIDDEN
            )

        image = self.get_object(pk)
        image.delete()

        return Response({"message": "Deleted Successfully"})