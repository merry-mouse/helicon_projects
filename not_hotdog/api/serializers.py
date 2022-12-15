from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from photoapp.models import Photo
 

class PhotoSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    
    class Meta:
        model = Photo
        fields = "__all__"


class PhotoDetailSerializerPutDelete(serializers.ModelSerializer):
 
    class Meta:
        model = Photo
        fields = ["id", "title", "not_hotdog_flag"]
