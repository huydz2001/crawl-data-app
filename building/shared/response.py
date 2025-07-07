from flask import jsonify

def make_response(success=True, data=None, message='', code=200):
    return jsonify({
        'success': success,
        'data': data,
        'message': message,
        'code': code
    }), code
