from flask import Blueprint, request
from auth.services import AuthService
from auth.schemas import *
from shared.decorators import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
@validate_input(LoginSchema)
def login():
    auth_service = AuthService()
    return auth_service.login(request.validated_data)

@auth_bp.route('/auth/register', methods=['POST'])
@validate_input(RegisterSchema)
def register():
    auth_service = AuthService()
    return auth_service.register(request.validated_data)

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    auth_service = AuthService()
    return auth_service.logout()

@auth_bp.route('/auth/refresh-token', methods=['POST'])
@validate_input(RefreshTokenSchema)
def refresh():
    auth_service = AuthService()
    return auth_service.refresh(request.validated_data)

@auth_bp.route('/auth/me', methods=['GET'])
def get_user_by_token():
    auth_service = AuthService()
    return auth_service.get_user_by_token()

@auth_bp.route('/auth/users', methods=['GET'])
@auth_required_with_role('admin')
def get_users():
    print(request.user)
    auth_service = AuthService()
    return auth_service.get_users()
