from api.kafka_producer import produce_message
from .models import Post
from rest_framework import serializers
from comment.serializers import CommentsSerializer


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        if not post:
            raise serializers.ValidationError("Post not created")

        produce_message(
            "blog_post_created", {"post_id": str(post.post_id), "content": post.content}
        )
        return post


class PostListSerializers(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
