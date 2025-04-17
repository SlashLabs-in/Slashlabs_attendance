import os
import datetime
import jwt
from functools import wraps
from flask import request, jsonify, current_app, redirect, url_for, flash
from flask_login import current_user

# Configuration for JWT
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
JWT_EXPIRATION_DELTA = datetime.timedelta(days=1)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_token(user_id):
    """
    Generate JWT token for API authentication
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')


def token_required(f):
    """
    Decorator for JWT token verification
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            from models import User
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'message': 'Invalid token. User not found.'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """
    Decorator to require admin role
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """
    Format datetime for template display
    """
    if value is None:
        return ""
    return value.strftime(format)
