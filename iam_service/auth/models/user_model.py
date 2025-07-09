from iam_service.common import BaseModel, db
from building.shared.utils import *

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

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "phone": self.phone,
            "email": self.email,
            "is_active": self.is_active,
            "role": self.role,
            "created_at": format_time(self.created_at),
            "created_by": self.created_by,
            "is_deleted": self.is_deleted,
        }
    
    def check_password(self, password):
        return verify_password(password, self.password)