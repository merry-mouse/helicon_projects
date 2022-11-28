from rest_framework import serializers
 
from photoapp.models import Photo
 
class ContactSerializer(serializers.ModelSerializer):
 
    class Meta:
 
        model = Photo
 
        fields = '__all__'