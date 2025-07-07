from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True  # Không tạo bảng cho class này
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_by = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)