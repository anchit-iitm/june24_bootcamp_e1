from app import create_app
# from app import app
from database.models import db
from app_security import user_datastore

app, api = create_app()

with app.app_context():
    db.drop_all()
    print('Dropped all tables')
    db.create_all()
    print('Created all tables')

    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='manager', description='Store manager role')
    user_datastore.find_or_create_role(name='customer', description='Store customer role')
    print('Created all roles')

    if not user_datastore.find_user(email='admin@a.com'):
        user_datastore.create_user(email='admin@a.com', password='password', roles=['admin', 'manager', 'customer'])

    if not user_datastore.find_user(email='manager@a.com'):
        user = user_datastore.create_user(email='manager@a.com', password='password')
        user_datastore.add_role_to_user(user, 'manager')
        user_datastore.add_role_to_user(user, 'customer')

    if not user_datastore.find_user(email='customer@a.com'):
        user = user_datastore.create_user(email='customer@a.com', password='password')
        user_datastore.add_role_to_user(user, 'customer')

    db.session.commit()
    
    print('Created admin and test users')