from shared.common import *
from datetime import datetime
from shared.app import db

class News(BaseModel):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "image": self.image,
            "type": self.type,
            "created_at": self.created_at,
        }