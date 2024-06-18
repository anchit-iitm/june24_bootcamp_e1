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

class DevelopmentConfig(Config):
    # Turn on debug mode
    DEBUG = True
    # Set the SQLite database directory to the development database
    SQLITE_DB_DIR = os.path.join(basedir, './database')
    # Set the SQLAlchemy database URI to the development database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'db.sqlite3')

    SECRET_KEY = 'super-secret'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'