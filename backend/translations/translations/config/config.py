from dotenv import load_dotenv
import os

load_dotenv()


DEBUG_MODE: str = eval(os.environ.get("FLASK_DEBUG", "true").title())

from translations.config.settings.brokers import *  # noqa
from translations.config.settings.storages import *  # noqa
from translations.config.settings.translations import *  # noqa


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://user:user1234@mysql-translations:3312/db_1"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DB_URI", "")


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://user:user1234@localhost:3313/db_test"
