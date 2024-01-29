from django.urls import path, include

urlpatterns = [
    path("blog/", include("blog.urls")),
    path("comment/", include("comment.urls")),
]
