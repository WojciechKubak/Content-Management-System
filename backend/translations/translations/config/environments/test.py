from translations.config.environments.base import *  # noqa
from translations.enums.enums import TranslationType, StorageType


DEBUG: bool = False
TESTING: bool = True

SQLALCHEMY_DATABASE_URI: str = "mysql://user:user1234@localhost:3309/db_1"

STORAGE_TYPE_STRATEGY: TranslationType = TranslationType.LOCAL
TRANSLATION_TYPE_STRATEGY: StorageType = StorageType.LOCAL
