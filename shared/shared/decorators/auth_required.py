from functools import wraps
from flask import request
import requests
from shared.ultis import make_response

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            make_response(success=False, message='Unauthorized', status=401)

        token = auth.split(' ')[1]
        try:
            res = requests.post('http://iam-service:5000/auth/verify', json={'token': token})
            if res.status_code != 200:
                make_response(success=False, message='Token invalid', status=401)
            request.user = res.json()
        except Exception:
            make_response(success=False, message='IAM not reachable', status=503)
        return f(*args, **kwargs)
    return wrapper
