from flask import Blueprint, request, jsonify
from iam_service.auth.services import AuthService
from iam_service.auth.schemas import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    login_schema = LoginSchema()
    login_data = login_schema.load(data)
    auth_service = AuthService()
    return auth_service.login(login_data)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    register_schema = RegisterSchema()
    register_data = register_schema.load(data)
    auth_service = AuthService()
    return auth_service.register(register_data)

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    auth_service = AuthService()
    return auth_service.logout()

@auth_bp.route('/auth/refresh-token', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token_schema = RefreshTokenSchema()
    refresh_token_data = refresh_token_schema.load(data)
    auth_service = AuthService()
    return auth_service.refresh(refresh_token_data)

@auth_bp.route('/auth/me', methods=['GET'])
def get_user_by_token():
    auth_service = AuthService()
    return auth_service.get_user_by_token()