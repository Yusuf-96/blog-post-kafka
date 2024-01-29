from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from blog.models import Post
from .serializers import CommentsSerializer


class CommentAPIView(APIView):
    def post(self, request):
        post_id = request.query_params.get("post_id")

        if not post_id:
            response = {
                "message": "Post id is required as parameter",
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.get(post_id=post_id)
        if not post:
            response = {
                "message": "Post not found",
                "status": status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        context_data = {"post_data": post}

        serializer = CommentsSerializer(data=request.data, context=context_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "status": status.HTTP_201_CREATED,
            "message": "You have comments sucessfully",
        }
        return Response(response, status=status.HTTP_201_CREATED)
