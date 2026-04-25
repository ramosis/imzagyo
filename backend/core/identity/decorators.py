from functools import wraps
from flask import request, jsonify, g
import jwt
from .service import IdentityService, get_jwt_secret, INNER_ROLES

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = IdentityService.get_current_user()
        if not user:
            return jsonify({'error': 'Login required'}), 401
        g.user = user
        return f(*args, **kwargs)
    return decorated

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = IdentityService.get_current_user()
            if not user or not IdentityService.has_permission(user['role'], permission):
                return jsonify({'error': 'Permission denied'}), 403
            g.user = user
            return f(*args, **kwargs)
        return decorated
    return decorator

def require_inner_circle(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = IdentityService.get_current_user()
        if not user or (user['role'] not in INNER_ROLES and not user.get('is_admin')):
            return jsonify({'error': 'Access restricted to inner circle'}), 403
        g.user = user
        return f(*args, **kwargs)
    return decorated
