from dotenv import load_dotenv
import ast
import os

load_dotenv()

class Config(object):
    """Base configuration class with common settings for all environments."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_SSL = ast.literal_eval(os.environ.get('MAIL_USE_SSL'))
    MAIL_USE_TLS = ast.literal_eval(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME =  os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD =  os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@mysql-users:3308/db_1'


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DB_URI', '')


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@localhost:3309/db_test'
