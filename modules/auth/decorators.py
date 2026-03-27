from functools import wraps
from flask import jsonify, g
from .service import AuthService

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = AuthService.get_current_user()
            if not user or not AuthService.has_permission(user.get('role'), permission):
                return jsonify({'error': f'Forbidden - Missing permission: {permission}'}), 403
            g.user = user
            return f(*args, **kwargs)
        return wrapper
    return decorator

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        g.user = user
        return f(*args, **kwargs)
    return wrapper

def require_inner_circle(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user or user.get('circle') != 'inner':
            return jsonify({'error': 'Unauthorized - Inner Circle Only'}), 403
        g.user = user
        return f(*args, **kwargs)
    return wrapper
# Legacy Aliases
circle_required = require_inner_circle
