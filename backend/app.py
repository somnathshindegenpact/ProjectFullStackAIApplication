from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
import os
import sys

sys.modules.setdefault('app', sys.modules[__name__])

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Allow browser-based frontend requests from any origin while keeping the API accessible.
    @app.before_request
    def handle_preflight():
        origin = request.headers.get('Origin')
        if request.method == 'OPTIONS' and origin:
            response = jsonify({})
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization,Content-Type,Accept'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
            response.status_code = 200
            return response

    # Add CORS headers to all responses so browser requests are accepted by the deployed app.
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers.setdefault('Access-Control-Allow-Headers', 'Authorization,Content-Type,Accept')
        response.headers.setdefault('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprints
    from auth import (
        bp as auth_bp,
        register as auth_register,
        login as auth_login,
        forgot_password as auth_forgot_password,
        reset_password as auth_reset_password,
        refresh as auth_refresh,
        me as auth_me,
    )
    from ai import bp as ai_bp
    from tasks import bp as tasks_bp
    from categories import bp as categories_bp
    from documents import bp as documents_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.add_url_rule('/api/auth/register', view_func=auth_register, methods=['POST'])
    app.add_url_rule('/api/auth/login', view_func=auth_login, methods=['POST'])
    app.add_url_rule('/api/auth/forgot-password', view_func=auth_forgot_password, methods=['POST'])
    app.add_url_rule('/api/auth/reset-password', view_func=auth_reset_password, methods=['POST'])
    app.add_url_rule('/api/auth/refresh', view_func=auth_refresh, methods=['POST'])
    app.add_url_rule('/api/auth/me', view_func=auth_me, methods=['GET'])
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(documents_bp, url_prefix='/api/documents')

    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    @app.errorhandler(Exception)
    def handle_uncaught_exception(error):
        import traceback
        traceback.print_exc()
        return jsonify({'msg': 'internal error', 'error': str(error)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    # Enable debug for local testing to see full tracebacks
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True, use_reloader=False)
