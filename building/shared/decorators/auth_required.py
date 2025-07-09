from functools import wraps
from flask import request
import requests
from shared.ultis import make_response

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return make_response(success=False, message='Unauthorized', status=401)

        token = auth.split(' ')[1]
        try:
            # Use RabbitMQ to verify token
            result = 'oke'

            if not result.get('success', False):
                return make_response(
                    success=False, 
                    message=result.get('message', 'Token invalid'), 
                    status=result.get('status', 401)
                )
        
            # Set user info from response
            request.user = result.get('data', {})
        except Exception:
            return make_response(success=False, message='IAM not reachable', status=503)
        return f(*args, **kwargs)
    return wrapper

def auth_required_with_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check auth first
            auth_result = auth_required(lambda: None)()
            
            # Check role
            user_role = request.user.get('role')
            if user_role != required_role:
                return make_response(
                    success=False, 
                    message='Insufficient permissions', 
                    status=403
                )
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
