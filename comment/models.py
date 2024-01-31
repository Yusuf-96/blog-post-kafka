import json
import time
import uuid
from django.db import models
from blog.models import Post
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from confluent_kafka import Producer


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

#     def should_auto_approve(self):
#         elapsed_time = (time.time() - self.created_at.timestamp()) / 60
#         return elapsed_time >= 3

#     def publish_to_kafka(self):
#         producer_conf = {
#             "bootstrap.servers": "localhost:9092",
#         }

#         producer = Producer(producer_conf)
#         comment_data = {
#             "comment_id": str(self.comment_id),
#             "post_id": str(self.post_id),
#             "created_at": str(self.created_at),
#             "text": self.text,
#         }

#         try:
#             producer.produce(
#                 "comment_topic", key=self.comment_id, value=json.dumps(comment_data)
#             )
#             producer.flush()

#             # Check if the comment should be auto-approved
#             if self.should_auto_approve():
#                 self.approved_comment = True
#                 self.save()
#                 print(f"Comment {self.comment_id} auto-approved after 5 minutes.")
#             else:
#                 print(f"Comment {self.comment_id} waiting for admin approval.")
#         except Exception as e:
#             print(f"Error publishing comment to Kafka: {e}")


# @receiver(post_save, sender=Comment)
# def comment_post_save(sender, instance, **kwargs):
#     # After saving a comment, publish it to Kafka
#     instance.publish_to_kafka()
