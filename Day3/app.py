from flask import Flask, jsonify, request
from flask_restful import Api

from database.models import db
from app_security import security, user_datastore
from config import DevelopmentConfig
from caching import cache

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)

    security.init_app(app, user_datastore)

    api = Api(app)

    cache.init_app(app)

    return app, api

app, api_handler = create_app()

@app.route('/helloWorld/<int:var2>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world(var2):
    return jsonify({'message':'Hello World', 'data': var2}), 200
    # if request.method == "post":
    #     pass

from routes.auth import helloWorld, login
api_handler.add_resource(helloWorld, '/api/helloWorld', '/api/helloWorld/<int:var1>')
api_handler.add_resource(login, '/api/login')

from routes.category import CategoryResource, CategorySpecific
api_handler.add_resource(CategoryResource, '/api/category')
api_handler.add_resource(CategorySpecific, '/api/category/<int:id>')


if __name__ == '__main__':
    app.run()