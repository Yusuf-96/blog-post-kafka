from .models import Post
from rest_framework import serializers
from comment.serializers import CommentsSerializer


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post


class PostListSerializers(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
