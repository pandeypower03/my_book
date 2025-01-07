from rest_framework import serializers
from .models import CustomUser
from .models import UploadedFiles

class userserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()




class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = [
            'id', 
            'book_title', 
            'book_description', 
            'visibility', 
            'cost', 
            'year_of_published', 
            'file_upload'
        ]