from .models import Post
from rest_framework import serializers


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post