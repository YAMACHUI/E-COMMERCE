from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != 'administrateur':
            return jsonify({"error": "Accès refusé: droits administrateur requis"}), 403
        return fn(*args, **kwargs)
    return wrapper