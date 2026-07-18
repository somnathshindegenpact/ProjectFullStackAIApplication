import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from config import config

sys.modules.setdefault('app', sys.modules[__name__])

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    frontend_origin = os.getenv('FRONTEND_ORIGIN', 'https://somnathshindegenpact.github.io')
    allowed_origins = {
        frontend_origin,
        'https://somnathshindegenpact.github.io',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:5000',
        'http://127.0.0.1:5000',
    }
    CORS(app, resources={r"/api/*": {"origins": list(allowed_origins)}}, supports_credentials=True, allow_headers=['Authorization', 'Content-Type', 'Accept'], methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])

    # Allow browser-based frontend requests from the configured origins.
    @app.before_request
    def handle_preflight():
        origin = request.headers.get('Origin')
        if request.method == 'OPTIONS' and origin:
            response = jsonify({})
            response.headers['Access-Control-Allow-Origin'] = origin if origin in allowed_origins else frontend_origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization,Content-Type,Accept'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
            response.status_code = 200
            return response

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if origin and origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        elif origin:
            response.headers['Access-Control-Allow-Origin'] = frontend_origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers.setdefault('Access-Control-Allow-Headers', 'Authorization,Content-Type,Accept')
        response.headers.setdefault('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    try:
        from models import User
    except ImportError:
        from .models import User

    with app.app_context():
        db.create_all()
        inspector = db.inspect(db.engine)
        existing_columns = {col['name'] for col in inspector.get_columns('users')}
        if 'reset_token' not in existing_columns:
            db.session.execute(db.text('ALTER TABLE users ADD COLUMN reset_token VARCHAR(255)'))
        if 'reset_token_expires_at' not in existing_columns:
            db.session.execute(db.text('ALTER TABLE users ADD COLUMN reset_token_expires_at DATETIME'))
        db.session.commit()

    def login_route():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'msg': 'email and password required'}), 400
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'msg': 'invalid credentials'}), 401
        access = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return jsonify({'access_token': access, 'refresh_token': refresh, 'user': {'id': user.id, 'email': user.email}})

    def register_route():
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

    def forgot_password_route():
        return jsonify({'msg': 'forgot-password endpoint unavailable'}), 501

    def reset_password_route():
        return jsonify({'msg': 'reset-password endpoint unavailable'}), 501

    def refresh_route():
        return jsonify({'msg': 'refresh endpoint unavailable'}), 501

    def me_route():
        return jsonify({'msg': 'me endpoint unavailable'}), 501

    app.add_url_rule('/api/auth/register', view_func=register_route, methods=['POST'])
    app.add_url_rule('/api/auth/login', view_func=login_route, methods=['POST'])
    app.add_url_rule('/api/auth/forgot-password', view_func=forgot_password_route, methods=['POST'])
    app.add_url_rule('/api/auth/reset-password', view_func=reset_password_route, methods=['POST'])
    app.add_url_rule('/api/auth/refresh', view_func=refresh_route, methods=['POST'])
    app.add_url_rule('/api/auth/me', view_func=me_route, methods=['GET'])

    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    @app.errorhandler(Exception)
    def handle_uncaught_exception(error):
        import traceback
        traceback.print_exc()
        return jsonify({'msg': 'internal error', 'error': str(error)}), 500

    return app


app = create_app()
application = app


if __name__ == '__main__':
    # Enable debug for local testing to see full tracebacks
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True, use_reloader=False)
