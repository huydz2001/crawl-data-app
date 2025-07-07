from flask import Blueprint, request, jsonify
from iam_service.auth.services import AuthService
from iam_service.auth.schemas import LoginSchema, RegisterSchema

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
    register_data = register_schema.load(data, return_data=True)
    print(f"After load type: {type(register_data)}")
    auth_service = AuthService()
    return auth_service.register(register_data)