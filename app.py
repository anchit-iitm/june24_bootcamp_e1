from flask import Flask, render_template, jsonify, make_response, request
from flask_security import auth_token_required, roles_accepted, current_user, verify_password

from database.models import db
from app_security import security, user_datastore

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'

# db = sqlalchemy(app)
db.init_app(app)

security.init_app(app, user_datastore)

# from database.models import User, Role
# role1 = Role(name='admin')
# db.session.add(role1)
# db.session.commit()

with app.app_context():
    db.create_all()

    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='manager', description='Store manager role')
    user_datastore.find_or_create_role(name='customer', description='Store customer role')
    db.session.commit()

    if not user_datastore.find_user(email='admin@a.com'):
        user_datastore.create_user(email='admin@a.com', password='password', roles=['admin', 'manager', 'customer'])
        db.session.commit()
    
    var24 = 'manager@abc.com'
    if not user_datastore.find_user(email=var24):
        user = user_datastore.create_user(email='manager@abc.com', password='password')
        user_datastore.add_role_to_user(user, 'manager')
        db.session.commit()
    
    if not user_datastore.find_user(email='manager1@abc.com'):
        user_datastore.create_user(email='manager1@abc.com', password='password', roles=['manager'], active=False)
        db.session.commit()

@app.route('/admin_token', methods=['POST'])  # login endpoint
def test_admin_token():
    # checks and all to verify if the user is present or not, then match the password
    admin_user = user_datastore.find_user(email='admin@a.com')
    token = admin_user.get_auth_token()
    print(admin_user)
    print('something')
    print(token)
    return jsonify({'token':admin_user.get_auth_token()})

@app.route('/token', methods=['POST'])  # login endpoint
def test_manager_token():
    # checks and all to verify if the user is present or not, then match the password
    admin_user = user_datastore.find_user(email='manager@abc.com')
    token = admin_user.get_auth_token()
    print(admin_user)
    print('something')
    print(token)
    return jsonify({'token':admin_user.get_auth_token()})


@app.route('/test')
# @auth_token_required
@roles_accepted('admin', 'customer', 'manager')
def test_protected():
    return jsonify({'message': 'You are authorized to view this page', 'user': current_user.email})

@app.route('/api/login', methods=['POST'])
def login_fn():
    data = request.get_json()
    email_var = data['email']
    password_var = data['password']
    user = user_datastore.find_user(email=email_var)
    if user :
        if verify_password(password_var, user.password):
            return jsonify({'message': 'login successful', 'token': user.get_auth_token(), 'email': user.email})
        return jsonify({'message': 'login failed, wrong password'})
    return jsonify({'message': 'login failed, user not found'})


    



@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def index():
    var1 = 'python variable'
    return render_template('index.html', var2=var1)

if __name__ == '__main__':
    app.run(debug=True)
