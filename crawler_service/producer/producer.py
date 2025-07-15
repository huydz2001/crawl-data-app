from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sample_data = [
    {"id": 1, "title": "Article A", "type": "news"},
    {"id": 2, "title": "Article B", "type": "blog"},
    {"id": 3, "title": "Article C", "type": "news"},
]

while True:
    for item in sample_data:
        producer.send("raw-data-topic", value=item)
        print("Sent:", item)
    producer.flush()
    time.sleep(10)
