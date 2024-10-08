from translations.config.env import env_to_bool
from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY: str = "secret-key"
DEBUG: bool = env_to_bool(os.environ.get("FLASK_DEBUG", True))
TESTING: bool = False

SQLALCHEMY_DATABASE_URI: str = (
    "mysql://user:user1234@db_articles_translations:3306/db_1"
)

from translations.config.settings.storages import *  # noqa
from translations.config.settings.messaging import *  # noqa
from translations.config.settings.translations import *  # noqa
