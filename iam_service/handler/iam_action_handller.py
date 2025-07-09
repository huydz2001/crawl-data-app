from building.shared.utils import *
from building.shared.response import make_response
from iam_service.auth.models import User

class IAMActionHandlers:
    @staticmethod
    def verify_token(request_data: dict) -> dict:
        try:
            token = request_data.get('token')

            decode_data = decode_token(token)
            user = User.query.filter_by(id=decode_data.get('user_id')).first()
            return user.to_dict()
        except Exception as e:
            return None