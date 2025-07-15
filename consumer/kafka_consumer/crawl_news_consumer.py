from kafka import KafkaConsumer
import json
from shared.app import create_app, db
from shared.config import DevConfig
from shared.models import News
import sys, os
import os

def crawl_news_consumer():
    kafka_broker_host = os.getenv("KAFKA_BROKER_HOST")
    kafka_broker_port = os.getenv("KAFKA_BROKER_PORT")

    consumer = KafkaConsumer(
        "crawl-data-filtered",
        bootstrap_servers=[f"{kafka_broker_host}:{kafka_broker_port}"],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="filtered-data-consumer"
    )

    print("[Consumer] Listening for messages...")

    for message in consumer:
        print("Received:", message.value)
        try:
            existsNews = News.query.filter_by(title=message.value["title"]).first()
            if existsNews:
                continue

            news = News(
                title=message.value["title"],
                url=message.value["url"],
                image=message.value["image"],
                type=message.value["type"]
            )
            db.session.add(news)
            db.session.commit()
        except Exception as e:
            print("Error saving to DB:", e)
