import os, secrets
from datetime import timedelta


# Import the os module to interact with the operating system
import os

# Define the base directory as the absolute path of the directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Define a base configuration class
class Config():
    # Turn off debug mode by default
    DEBUG = False
    # Set the SQLite database directory to None by default
    SQLITE_DB_DIR = None
    # Set the SQLAlchemy database URI to None by default
    SQLALCHEMY_DATABASE_URI = None
    # Turn off SQLAlchemy's event system, which can consume a lot of resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Define a development configuration class that inherits from the base configuration class
class LocalDev(Config):
    # Set the SQLite database directory to the db directory in the base directory
    SQLITE_DB_DIR = os.path.join(basedir, './database')
    # Set the SQLAlchemy database URI to the SQLite database in the db directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'db.sqlite3')  # Required for the application to work

    # Set the secret key for Flask-Security
    SECRET_KEY = 'your-secret-key'
    # Enable user tracking in Flask-Security
    SECURITY_TRACKABLE = True    
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

    SECURITY_LOGIN_URL = '/ABCD'


    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 60

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'no-reply@grocerystore.com'

    DEBUG = True