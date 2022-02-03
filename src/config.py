from dotenv import dotenv_values
from os import environ
from pymongo import MongoClient

DOT_ENV = dotenv_values('.env')


def get_db():
    db_user = DOT_ENV['DB_USER']
    db_password = DOT_ENV['DB_PASSWORD']
    db_cluster = DOT_ENV['DB_CLUSTER']
    db_name = DOT_ENV['DB_NAME']

    connection = 'mongodb+srv://{}:{}@{}.hstfi.mongodb.net/{}?retryWrites=true&w=majority'.format(
        db_user,
        db_password,
        db_cluster,
        db_name
    )
    client = MongoClient(connection)

    return client[db_name]


class Config:
    PORT = DOT_ENV['PORT']
    DB = get_db()
    USER_COLLECTION = DB.usercollection
    SECRET_KEY = DOT_ENV['SECRET_KEY']
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True

