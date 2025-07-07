from iam_service.auth.models import User
from iam_service.auth.schemas import LoginSchema, RegisterSchema
from iam_service.common import db
from building.shared.exceptions import *
from building.shared.response import make_response
from building.shared.utils import hash_password, verify_password, create_token

class AuthService:
    def register(self, user_data):
        try:
            user = User(
                username=user_data['username'],
                phone=user_data['phone'],
                password=hash_password(user_data['password']),
                email=user_data['email'],
                role=user_data['role']
            )
            db.session.add(user)
            db.session.commit()
            return make_response(True, user.to_dict(), 'User registered successfully', 201)
        except Exception as e:
            db.session.rollback()
            raise InternalServerError(e)

    def login(self, login_data: LoginSchema):
        try:
            user = User.query.filter_by(username=login_data['username']).first()
            if not user:
                raise NotFoundError('User not found')
            if not user.check_password(login_data['password']):
                raise BadRequestError('Invalid password')
            token = create_token({
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            })
            return make_response(True, token, 'Login successfully', 200)
        except Exception as e:
            raise InternalServerError(e)