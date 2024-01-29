import uuid
from django.db import models
from blog.models import Post
from django.utils import timezone


class Comment(models.Model):
    comment_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        db_table = "comments"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.text
