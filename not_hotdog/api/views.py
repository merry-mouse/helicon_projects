from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from photoapp.models import Photo
from .serializers import PhotoSerializer, PhotoDetailSerializerPutDelete
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAdminUser
 

class PhotoList(APIView):
    """
    List all photos, or create a new photo.
    """
    def get(self, request, format=None):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

class PhotoDetailGetView(APIView):
    """
    Retrieve a photo instance.
    """
    permission_classes = (IsAdminUser,)
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)


class PhotoDetailPutDeleteView(APIView):
    """
    Update, delete a photo instance.
    """
    permission_classes = (IsAdminUser,)
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise Http404


    def put(self, request, pk, format=None):
        photo = self.get_object(pk)
        serializer = PhotoDetailSerializerPutDelete(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        photo = self.get_object(pk)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)