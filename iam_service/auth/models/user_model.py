from iam_service.common import BaseModel, db

class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)