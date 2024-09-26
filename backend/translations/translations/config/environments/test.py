from translations.config.environments.base import *  # noqa
from translations.enums.enums import TranslationType, StorageType
from sqlalchemy.pool import Pool, NullPool
import os


DEBUG: bool = False
TESTING: bool = True

SQLALCHEMY_DATABASE_URI: str = "mysql://user:user1234@localhost:3309/db_1"

if os.environ.get("GITHUB_WORKFLOW"):
    SQLALCHEMY_DATABASE_URI: str = "mysql://user:password@127.0.0.1:3306/test_db"

SQLALCHEMY_ECHO: bool = False
SQLALCHEMY_ENGINE_OPTIONS: dict[str, Pool] = {"poolclass": NullPool}

STORAGE_TYPE_STRATEGY: TranslationType = TranslationType.LOCAL
TRANSLATION_TYPE_STRATEGY: StorageType = StorageType.LOCAL

SERVER_NAME: str = "localhost.localdomain"
APPLICATION_ROOT: str = "/"
PREFERRED_URL_SCHEME: str = "http"
