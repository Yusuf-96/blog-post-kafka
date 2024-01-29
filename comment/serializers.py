from rest_framework import serializers
from .models import Comment


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'text']

    def create(self, validated_data):
        post_data = self.context["post_data"]

        return Comment.objects.create(**validated_data, post=post_data)
