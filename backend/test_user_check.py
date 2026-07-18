from app import create_app
from models import User

app = create_app()
with app.app_context():
    u = User.query.filter_by(email='demo@example.com').first()
    print('User found:', bool(u))
    if u:
        print('Password ok:', u.check_password('password'))
