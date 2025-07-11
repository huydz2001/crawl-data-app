from common import BaseModel, db
from datetime import datetime

class Token(BaseModel):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=True)
    refresh_token = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }
    
    def delete_token(self, token):
        token = Token.query.filter_by(access_token=token).first()
        if token:
            token.access_token = None
            token.refresh_token = None
            token.updated_at = datetime.now()
            db.session.commit()

    def update_token(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.updated_at = datetime.now()
        db.session.commit()