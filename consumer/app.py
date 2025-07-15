from shared.app import create_app, db
from shared.models import *
from shared.config import DevConfig
from kafka_consumer.crawl_news_consumer import crawl_news_consumer

app = create_app(DevConfig)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        crawl_news_consumer()

    app.run(host="0.0.0.0", port=5000)
