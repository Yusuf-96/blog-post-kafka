from rest_framework import serializers

from api.kafka_producer import produce_message
from .models import Comment


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment_id", "text", "approved_comment", "created_at"]

    def create(self, validated_data):
        post_data = self.context["post_data"]

        instance = Comment.objects.create(**validated_data, post=post_data)
        


        produce_message(
            "comment_topic",
            {
                "comment_id": str(instance.comment_id),
                "post_id": str(instance.post),
                "content": instance.text,
            },
        )

        return instance
