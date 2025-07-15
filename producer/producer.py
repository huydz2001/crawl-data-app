from kafka import KafkaProducer
import json
import time
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

kafka_broker_host = os.getenv("KAFKA_BROKER_HOST")
kafka_broker_port = os.getenv("KAFKA_BROKER_PORT")
print(f"Kafka broker host: {kafka_broker_host}, port: {kafka_broker_port}")

producer = KafkaProducer(
    bootstrap_servers=[f"{kafka_broker_host}:{kafka_broker_port}"],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def crawl_vnexpress():
    url = "https://vnexpress.net/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []
    for item in soup.select("article.item-news"):
        title_tag = item.select_one("h3.title-news a")
        img_tag = item.select_one("img")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            img_url = img_tag['data-src'] if img_tag and img_tag.has_attr('data-src') else (img_tag['src'] if img_tag and img_tag.has_attr('src') else None)
            articles.append({
                "title": title,
                "url": link,
                "image": img_url,
                "type": "news"
            })
    return articles

articles = crawl_vnexpress()

while True:
    for item in articles:
        producer.send("crawl-data", value=item)
        print("Sent:", item)
    producer.flush()
    time.sleep(60)
