from translations.env_config import S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET_NAME
from translations.storage.boto3 import Boto3Service


boto3_service = Boto3Service(S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_BUCKET_NAME)
