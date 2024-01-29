from django.db import models
import uuid


class Post(models.Model):
    post_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return self.content
