from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from shared.config import DevConfig

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app
