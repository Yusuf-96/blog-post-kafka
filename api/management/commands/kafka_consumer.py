import json
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from confluent_kafka import Consumer, KafkaException
from comment.models import Comment


class Command(BaseCommand):
    help = "Consume comments from Kafka and process them"

    def handle(self, *args, **options):
        consumer_conf = {
            "bootstrap.servers": "localhost:9092",
            "group.id": "blog_post_consumer_group",
            "auto.offset.reset": "earliest",
        }

        consumer = Consumer(consumer_conf)
        consumer.subscribe(["blog_post_created", "comment_topic"])

        try:
            while True:
                try:
                    msg = consumer.poll(1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaException._PARTITION_EOF:
                            continue
                        else:
                            print(msg.error())
                            break
                    payload = json.loads(msg.value())
                    comment_id = payload.get("comment_id")
                    if msg.topic() == "comment_topic" and comment_id:
                        try:
                            comment = Comment.objects.get(
                                comment_id=comment_id, approved_comment=False
                            )
                            # Introduce a 5-minute delay before processing
                            time.sleep(120)
                            # Logic for sending notification or other actions
                            comment.approved_comment = True
                            comment.save()
                            print("Received and auto-approved comment:", payload)
                        except Comment.DoesNotExist:
                            print(f"Comment {comment_id} not found.")
                except Exception as e:
                    print(f"Error processing comment: {e}")

        except KeyboardInterrupt:
            print("Keyboard interrupt. Stopping the consumer.")

        finally:
            consumer.close()
