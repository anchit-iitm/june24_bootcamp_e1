from flask_security import Security, SQLAlchemyUserDatastore

from database.models import db, User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()