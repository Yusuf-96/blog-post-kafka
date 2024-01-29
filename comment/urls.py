from django.urls import path
from . import views


urlpatterns = [path("comments", views.CommentAPIView().as_view())]
