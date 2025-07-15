from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "filtered-data-topic",
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="filtered-data-consumer"
)

print("Listening for messages on 'filtered-data-topic'...")

for message in consumer:
    print("Received:", message.value)