from iam_service.auth.models import User
from iam_service.auth.schemas import LoginSchema, RegisterSchema
from building.shared.exceptions import *
from building.shared.response import make_response

class AuthService:
    def register(self, user_data: RegisterSchema):
        try:
            user = User(
                username=user_data.username,
                phone=user_data.phone,
                password=user_data.password,
                email=user_data.email,
                role=user_data.role
            )
            user.save()
            make_response(user, 201)
        except Exception as e:
            raise InternalServerError(e)

    def login(self, login_data: LoginSchema):
        try:
            user = User.query.filter_by(username=login_data.username).first()
            if not user:
                raise NotFoundError('User not found')
            if not user.check_password(login_data.password):
                raise BadRequestError('Invalid password')
            token = create_token(user.id)
            make_response(token, 200)
        except Exception as e:
            raise InternalServerError(e)