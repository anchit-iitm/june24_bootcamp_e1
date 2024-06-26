from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_security import verify_password, login_user, roles_accepted, current_user, logout_user

from database.models import user_datastore, db

class hello(Resource):
    def post(self, var2):
        return jsonify({"message": "Hello, World!", "data": var2})

    def get(self):
        return jsonify({"message": "Hello, World!"})

    def put(self):
        return jsonify({"message": "Hello, World! put"})

    def delete(self):
        return jsonify({"message": "Hello, World!"})
    
class login(Resource):
    def post(self):
        data = request.get_json()
        # email = data.get('email')
        email = data['email']
        password = data['password']
        print(email, password)
        user = user_datastore.find_user(email=email)
        if user:
            if verify_password(password, user.password):
                login_user(user)
                db.session.commit()
                token = user.get_auth_token()
                # return make_response(jsonify({'token': token, 'email': user.email, 'id': user.id, 'roles': [role.name for role in user.roles]}), 200)
                role = 'admin' if current_user.has_role('admin') else 'manager' if current_user.has_role('manager') else 'customer'
                print(role)
                return make_response(jsonify({'token': token, 'email': user.email, 'id': user.id, 'role': role, 'message': 'login successful'}), 200)
            return make_response(jsonify({'message': 'password doesnt match', 'password': password}), 401)
        return make_response(jsonify({'message': 'user not present', 'email': email}), 404)
    
class register(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        role = data['role']
        if not email:
            return make_response(jsonify({"message": "email is required"}), 400)
        if not password:
            return make_response(jsonify({"message": "password is required"}), 400)
        if not role:
            return make_response(jsonify({"message": "role is required"}), 400)
        # username = email.split('@')[0]
        
        
        user = user_datastore.find_user(email=email)
        if user:
            return make_response(jsonify({"message": "user already present", "email": user.email}), 400)
        
        user = user_datastore.create_user(email=email, password=password)
        if role == 'manager':
            user_datastore.deactivate_user(user)
            user_datastore.add_role_to_user(user, 'manager')
            user_datastore.add_role_to_user(user, 'customer')
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
        return make_response(jsonify({"message": "user created successfully", "email": user.email}), 201)
    
class logout(Resource):
    @roles_accepted('admin', 'manager', 'customer')
    def post(self):
        user = user_datastore.find_user(id=current_user.id)
        if not user:
            return make_response(jsonify({"message": "No user found by that id"}), 404)
        logout_user(user)
        db.session.commit()
        return make_response(jsonify({"message": "user logged out successfully", "email": user.email}), 200)
