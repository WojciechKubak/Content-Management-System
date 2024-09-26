from translations.config.environments.base import *  # noqa
import os


SECRET_KEY: str = os.environ["FLASK_SECRET_KEY"]

SQLALCHEMY_DATABASE_URI: str = os.environ.get(
    "PRODUCTION_DB_URI", "mysql://user:user1234@db_articles_translations:3306/db_1"
)

PREFERRED_URL_SCHEME: str = "https"
SESSION_COOKIE_SECURE: bool = True
REMEMBER_COOKIE_SECURE: bool = True
