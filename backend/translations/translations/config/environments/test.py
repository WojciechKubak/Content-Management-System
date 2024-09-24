from translations.config.environments.base import *  # noqa
from translations.enums.enums import TranslationType, StorageType
from sqlalchemy.pool import NullPool


DEBUG: bool = False
TESTING: bool = True

SQLALCHEMY_DATABASE_URI: str = "mysql://user:user1234@localhost:3309/db_1"
SQLALCHEMY_ECHO: bool = False
SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": NullPool}

STORAGE_TYPE_STRATEGY: TranslationType = TranslationType.LOCAL
TRANSLATION_TYPE_STRATEGY: StorageType = StorageType.LOCAL

SERVER_NAME: str = "localhost.localdomain"
APPLICATION_ROOT: str = "/"
PREFERRED_URL_SCHEME: str = "http"
