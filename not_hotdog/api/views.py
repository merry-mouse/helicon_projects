from rest_framework import status
 
from rest_framework.decorators import api_view
 
from rest_framework.response import Response

from photoapp.models import Photo
 
from .serializers import ContactSerializer
 
@api_view(['GET'])
 
def photo_list(request):
    if request.method == 'GET':
 
        photos = Photo.objects.all()
 
        serializer = ContactSerializer(photos, many=True)
 
        return Response(serializer.data)
 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
