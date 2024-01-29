from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostListSerializers, PostSerializers
from rest_framework import status


class CreatePostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializers(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_201_CREATED,
                "message": "Post has been created sucessfully",
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "You did not post yet",
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
