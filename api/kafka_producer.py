from confluent_kafka import Producer
import json


def delivery_report(err, msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))


def produce_message(topic, message):
    producer.produce(
        topic, key="key", value=json.dumps(message), callback=delivery_report
    )
    producer.poll(0)


producer_conf = {
    "bootstrap.servers": "localhost:9092",
}

producer = Producer(producer_conf)
