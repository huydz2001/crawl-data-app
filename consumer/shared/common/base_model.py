from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from shared.app import db

class BaseModel(db.Model):
    __abstract__ = True  # Không tạo bảng cho class này
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    # created_by = db.Column(db.String(50))
    # updated_by = db.Column(db.String(50))
    # is_deleted = db.Column(db.Boolean, default=False)