from dotenv import load_dotenv
import os

load_dotenv()


DEBUG_MODE: str = eval(os.environ.get("FLASK_DEBUG", "true").title())

DEFAULT_DEV_DATABASE_URI: str = (
    "mysql://user:user1234@db_articles_translations:3306/db_1"
)
DEFAULT_TEST_DATABASE_URI: str = "mysql://user:user1234@localhost:3309/db_1"

from translations.config.settings.brokers import *  # noqa
from translations.config.settings.storages import *  # noqa
from translations.config.settings.translations import *  # noqa


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG: bool = False
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URI: str = DEFAULT_DEV_DATABASE_URI


class ProductionConfig(Config):
    DEBUG: bool = False
    TESTING: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        env_db = os.environ.get("PRODUCTION_DB_URI")
        return env_db if env_db else DEFAULT_DEV_DATABASE_URI


class TestingConfig(Config):
    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = DEFAULT_TEST_DATABASE_URI
