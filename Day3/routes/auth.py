from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_security import verify_password

from app_security import user_datastore


class helloWorld(Resource):
    def get(self):
        return make_response(jsonify({'message': 'hello world'}), 200)
    
    def post(self, var1):
        return jsonify({'message': 'hello world post method', 'data': var1})

    def put(self):
        return jsonify({'message': 'hello world putt method'})
    
    def delete(self):
        return jsonify({'message': 'hello world delete method'})
    
class login(Resource):
    def post(self):
        data = request.get_json()
        email_var = data['email']
        password_var = data['password']
        user = user_datastore.find_user(email=email_var)
        if user :
            if verify_password(password_var, user.password):
                return jsonify({'message': 'login successful', 'token': user.get_auth_token(), 'email': user.email})
            return jsonify({'message': 'login failed, wrong password'})
        return jsonify({'message': 'login failed, user not found'})
        
    
