from flask import Flask, jsonify, request
from flask_security import verify_password
from flask_restful import Api
from flask_cors import CORS 
 
from config import LocalDev
from database.models import db, user_datastore
from app_security import security

# app = Flask(__name__)
# app.config.from_object(LocalDev)
# db.init_app(app)
# security.init_app(app, user_datastore)

def create_celery(app1):
    from celery import Celery
    celery = Celery(app1.import_name)
    import celery_config 
    celery.config_from_object(celery_config)
    return celery

def create_app():

    app = Flask(__name__)
    app.config.from_object(LocalDev)

    db.init_app(app)

    security.init_app(app, user_datastore)

    api = Api(app)

    CORS(app)

    from caching import cache  # lazy importing because cache is not used in this file else where

    cache.init_app(app)
    celery = create_celery(app)

    from mailer import mail

    mail.init_app(app)

    return app, api, celery

app, api_handler, celery_app = create_app()
import celery_tasks

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    # 'trigger-add-helloWorld-every-10-seconds':{
    #     'task': 'celery_tasks.helloWorld',
    #     'schedule': 10.0,
    # },
    # 'trigger-add-add-every-10-seconds':{
    #     'task': 'celery_tasks.add',
    #     'schedule': 5.0,
    #     'args': (10, 20)
    # },
    'trigger-add-fetch_X_category-daily-21-06':{
        'task': 'celery_tasks.fetch_X_category',
        'schedule': crontab(hour=21, minute=10),
        'args': (1,)
    },
    'trigger-monthly-mail':{
        'task': 'celery_tasks.monthly_mail_demo',
        'schedule': crontab(day_of_month=29, hour=21, minute=37)
    }
}

@app.route("/hello_world/<int:var2>", methods=["GET", "POST", "PUT", "DELETE"])
def hello_world(var2):
    return jsonify({"message": "Hello, World!", "data": var2})

'''@app.route('/login', methods=['POST'])
def login_():
    data = request.get_json()
    # email = data.get('email')
    email = data['email']
    password = data['password']
    user = user_datastore.find_user(email=email)
    if user:
        if verify_password(password, user.password):
            token = user.get_auth_token()
            return jsonify({'token': token, 'email': user.email})
        return jsonify({'message': 'password doesnt match'}), 401
    return jsonify({'message': 'user not present'}), 401'''


from routes.auth import hello, login, register
api_handler.add_resource(hello, '/api/hello_world/<int:var2>')
api_handler.add_resource(login, '/api/login')
api_handler.add_resource(register, '/api/register')

from routes.category import CategoryResource, CategorySpecific
api_handler.add_resource(CategoryResource, '/api/category')
api_handler.add_resource(CategorySpecific, '/api/category/<int:id>')

from routes.product import ProductResource, ProductSpecific
api_handler.add_resource(ProductResource, '/api/product')
api_handler.add_resource(ProductSpecific, '/api/product/<int:id>')

from routes.admin import CategoryDelete, ProductDelete, toggle_user_status, UserResources
api_handler.add_resource(CategoryDelete, '/api/category_delete/<int:id>')
api_handler.add_resource(ProductDelete, '/api/product_delete/<int:id>')
api_handler.add_resource(toggle_user_status, '/api/toggle_user_status/<int:id>')
api_handler.add_resource(UserResources, '/api/users', '/api/user/<int:id>')

from routes.celery_routes import celeryHello
api_handler.add_resource(celeryHello, '/api/celery_hello', '/api/celery_hello/<int:y>')

with app.app_context():
    # user_datastore.find_or_create_role(name='admin', description='Administrator')
    # if not user_datastore.find_user(email='admin@a.com'):
    #     user_datastore.create_user(email='admin@a.com', password='admin', roles=['admin'])
        
    # db.session.commit()
    pass

if __name__ == "__main__":
    app.run()