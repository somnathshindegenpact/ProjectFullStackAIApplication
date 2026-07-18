from app import create_app, db
from models import User, Category, Task, Document


def seed(app):
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='demo@example.com').first():
            u = User(email='demo@example.com')
            u.set_password('password')
            db.session.add(u)
            db.session.commit()
            c1 = Category(user_id=u.id, name='Work', color='#ff7f50')
            c2 = Category(user_id=u.id, name='Personal', color='#4caf50')
            db.session.add_all([c1, c2])
            db.session.commit()
            t = Task(user_id=u.id, category_id=c1.id, title='Finish project pitch', description='Refine scope and write README')
            db.session.add(t)
            db.session.commit()
            d = Document(user_id=u.id, title='Example Notes', content='This document contains example notes for the user.', source_url='')
            db.session.add(d)
            db.session.commit()
            print('Seeded demo user: demo@example.com / password')
        else:
            print('Demo user already exists')


if __name__ == '__main__':
    app = create_app()
    seed(app)
