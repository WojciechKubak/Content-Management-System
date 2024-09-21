from translations.enums.enums import StorageType
from translations.config.env import PROJECT_ROOT
from translations.config.env import env_to_enum
import os


STORAGE_TYPE_STRATEGY: StorageType = env_to_enum(
    StorageType, os.getenv("STORAGE_TYPE", StorageType.LOCAL.value)
)

if STORAGE_TYPE_STRATEGY == StorageType.LOCAL:
    MEDIA_ROOT_NAME: str = "media"
    MEDIA_ROOT: str = os.path.join(PROJECT_ROOT, MEDIA_ROOT_NAME)

if STORAGE_TYPE_STRATEGY == StorageType.S3:
    AWS_S3_ACCESS_KEY_ID: str = os.getenv("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY: str = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET_NAME: str = os.getenv("AWS_S3_BUCKET_NAME")
