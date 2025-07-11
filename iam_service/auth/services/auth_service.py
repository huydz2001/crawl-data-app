from iam_service.auth.models import *
from iam_service.auth.schemas import *
from iam_service.common import db
from building.shared.exceptions import *
from building.shared.response import make_response
from building.shared.utils import *
from flask import request
from datetime import datetime

class AuthService:
    def register(self, user_data):
        try:
            # Check if phone already exists
            existing_phone = User.query.filter_by(phone=user_data['phone']).first()
            if existing_phone:
                raise BadRequestError('Phone number already exists')
            
            # Check if email already exists
            existing_email = User.query.filter_by(email=user_data['email']).first()
            if existing_email:
                raise BadRequestError('Email already exists')
            
            # Check if username already exists
            existing_username = User.query.filter_by(username=user_data['username']).first()
            if existing_username:
                raise BadRequestError('Username already exists')
            
            user = User(
                username=user_data['username'],
                phone=user_data['phone'],
                password=hash_password(user_data['password']),
                email=user_data['email'],
                role=user_data['role'],
                created_at=datetime.now(),
            )
            db.session.add(user)
            db.session.commit()
            return make_response(True, user.to_dict(), 'User registered successfully', 201)
        except Exception as e:
            db.session.rollback()
            raise

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
            refresh_token = create_refresh_token({
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            })
            token_model = Token.query.filter_by(user_id=user.id).first()
            if token_model:
                token_model.access_token = token
                token_model.refresh_token = refresh_token
                token_model.updated_by = user.id
                
                db.session.commit()
            else:
                token_model = Token(
                    access_token=token,
                    refresh_token=refresh_token,
                    user_id=user.id,
                    created_by=user.id,
                    updated_by=user.id
                )

                db.session.add(token_model)
                db.session.commit()
            return make_response(True, {'access_token': token, 'refresh_token': refresh_token}, 'Login successfully', 200)
        except Exception as e:
            db.session.rollback()
            raise
    
    def logout(self):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            if not token:
                raise BadRequestError('Token is required')
            token_model = Token.query.filter_by(access_token=token).first()
            if not token_model:
                raise NotFoundError('Token not found')
            token_model.delete_token(token)
            return make_response(True, None, 'Logout successfully', 200)
        except Exception as e:
            db.session.rollback()
            raise

    def refresh(self, refresh_token_data: RefreshTokenSchema):
        try:
            token_model = Token.query.filter_by(refresh_token=refresh_token_data['refresh_token']).first()
            if not token_model:
                raise NotFoundError('Refresh token is invalid')
            
            decoded_token = decode_token(refresh_token_data['refresh_token'])
            user_id = decoded_token['user_id']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise NotFoundError('User not found')
            
            token = create_token({
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            })
            refresh_token = create_refresh_token({
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            })

            token_model.update_token(token, refresh_token)
            return make_response(True, {'access_token': token, 'refresh_token': refresh_token}, 'Refresh token successfully', 200)
        except Exception as e:
            db.session.rollback()
            raise

    def get_user_by_token(self):
        try:
            token = request.headers.get('Authorization')
            if not token:
                raise UnauthorizedError('Unauthorized')
            token = token.split(' ')[1]
            if not token:
                raise UnauthorizedError('Unauthorized')
            decoded_token = decode_token(token)
            if not decoded_token:
                raise UnauthorizedError('Unauthorized')


            user_id = decoded_token['user_id']
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise NotFoundError('User not found')
            return make_response(True, user.to_dict(), 'User found', 200)
        except Exception as e:
            raise
    