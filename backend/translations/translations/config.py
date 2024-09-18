import os


class Config(object):
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration class for the development environment."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql://user:user1234@mysql-translations:3312/db_1"


class ProductionConfig(Config):
    """Configuration class for the production environment."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DB_URI", "")


class TestingConfig(Config):
    """Configuration class for the testing environment."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://user:user1234@localhost:3313/db_test"
    SERVER_NAME = "localhost.localdomain"
    APPLICATION_ROOT = "/"
    PREFERRED_URL_SCHEME = "http"
