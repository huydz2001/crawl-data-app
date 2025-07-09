from functools import wraps
from flask import request
from shared.ultis import make_response

def validate_input(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            try:
                schema().load(json_data)
            except Exception as e:
                return make_response(success=False, message=str(e), status=400)
            return f(*args, **kwargs)
        return wrapper
    return decorator