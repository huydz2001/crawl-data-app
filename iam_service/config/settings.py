import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///auth.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'admin123')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False