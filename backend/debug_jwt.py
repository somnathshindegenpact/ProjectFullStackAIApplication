from app import create_app
from flask_jwt_extended import create_access_token

app = create_app()
with app.app_context():
    print('Config JWT_SECRET_KEY:', app.config.get('JWT_SECRET_KEY'))
    print('Creating token...')
    t = create_access_token(identity=1)
    print('Token length:', len(t))
