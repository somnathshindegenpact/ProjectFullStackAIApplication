import os
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from models import User

bp = Blueprint('auth', __name__)

RATE_LIMIT_WINDOW_SECONDS = int(os.getenv('RATE_LIMIT_WINDOW_SECONDS', 300))
RATE_LIMIT_MAX_ATTEMPTS = int(os.getenv('RATE_LIMIT_MAX_ATTEMPTS', 5))

login_attempts = {}


def _rate_limit_key(ip_address, email=None):
    return f"{ip_address}:{(email or '').lower()}"


def _is_rate_limited(ip_address, email=None):
    key = _rate_limit_key(ip_address, email)
    now = datetime.utcnow()
    attempts = login_attempts.get(key, [])
    attempts = [ts for ts in attempts if now - ts < timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS)]
    login_attempts[key] = attempts
    return len(attempts) >= RATE_LIMIT_MAX_ATTEMPTS


def _record_attempt(ip_address, email=None):
    key = _rate_limit_key(ip_address, email)
    now = datetime.utcnow()
    attempts = login_attempts.get(key, [])
    attempts = [ts for ts in attempts if now - ts < timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS)]
    attempts.append(now)
    login_attempts[key] = attempts


def _clear_attempts(ip_address, email=None):
    key = _rate_limit_key(ip_address, email)
    login_attempts.pop(key, None)


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'msg': 'email and password required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'email already registered'}), 400

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return jsonify({'access_token': access, 'refresh_token': refresh, 'user': {'id': user.id, 'email': user.email}}), 201


@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr or 'unknown')
        if not email or not password:
            return jsonify({'msg': 'email and password required'}), 400

        if _is_rate_limited(ip_address, email):
            return jsonify({'msg': 'too many login attempts, please try again later'}), 429

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            _record_attempt(ip_address, email)
            return jsonify({'msg': 'invalid credentials'}), 401

        _clear_attempts(ip_address, email)
        access = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return jsonify({'access_token': access, 'refresh_token': refresh, 'user': {'id': user.id, 'email': user.email}})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'msg': 'internal error', 'error': str(e)}), 500


@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'msg': 'email required'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        token = secrets.token_urlsafe(24)
        user.reset_token = token
        user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

    return jsonify({'msg': 'If an account exists for that email, a reset link has been sent.'})


@bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    token = data.get('token')
    new_password = data.get('password')
    if not token or not new_password:
        return jsonify({'msg': 'token and password required'}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expires_at or user.reset_token_expires_at < datetime.utcnow():
        return jsonify({'msg': 'invalid or expired reset token'}), 400

    user.set_password(new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    db.session.commit()
    return jsonify({'msg': 'password updated successfully'})


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return jsonify({'access_token': access})


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = User.query.get(identity)
    if not user:
        return jsonify({'msg': 'user not found'}), 404
    return jsonify({'id': user.id, 'email': user.email})
