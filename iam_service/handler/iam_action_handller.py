from shared.utils import *
from shared.response import make_response
from auth.models import User

class IAMActionHandlers:
    @staticmethod
    def verify_token(request_data: dict) -> dict:
        try:
            token = request_data.get('token')

            decode_data = decode_token(token)
            user = User.query.filter_by(id=decode_data.get('user_id'), is_deleted=False, is_active=True).first()
            return user.to_basic_dict()
        except Exception as e:
            return None