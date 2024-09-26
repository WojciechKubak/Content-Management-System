from translations.common.utils import assert_settings
from translations.core.exceptions import StorageError
from botocore.exceptions import BotoCoreError, ClientError
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Self
import boto3


@dataclass
class S3Credentials:
    access_key_id: str
    secret_access_key: str
    bucket_name: str


@dataclass
class ResponseMetadata:
    request_id: str
    host_id: str
    http_status_code: int
    http_headers: dict[str, str]
    retry_attempts: int

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> Self:
        return cls(
            request_id=response["RequestId"],
            host_id=response["HostId"],
            http_status_code=response["HTTPStatusCode"],
            http_headers=response["HTTPHeaders"],
            retry_attempts=response["RetryAttempts"],
        )


@dataclass
class PutObjectResponse:
    response_metadata: ResponseMetadata
    etag: str
    server_side_encryption: str

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> Self:
        response_metadata = ResponseMetadata.from_response(response["ResponseMetadata"])
        return cls(
            response_metadata=response_metadata,
            etag=response["ETag"],
            server_side_encryption=response.get("ServerSideEncryption", ""),
        )


@lru_cache
def s3_get_credentials() -> S3Credentials:
    settings = assert_settings(
        [
            "AWS_S3_ACCESS_KEY_ID",
            "AWS_S3_SECRET_ACCESS_KEY",
            "AWS_S3_BUCKET_NAME",
        ],
        "AWS S3 credentials not found",
    )

    return S3Credentials(
        access_key_id=settings["AWS_S3_ACCESS_KEY_ID"],
        secret_access_key=settings["AWS_S3_SECRET_ACCESS_KEY"],
        bucket_name=settings["AWS_S3_BUCKET_NAME"],
    )


def s3_get_client() -> boto3.client:
    credentials = s3_get_credentials()

    return boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )


def text_to_file_upload(
    *, file_name: str, content: str, extension: str = ".txt"
) -> PutObjectResponse:
    s3 = s3_get_client()
    credentials = s3_get_credentials()

    try:
        response = s3.put_object(
            Bucket=credentials.bucket_name,
            Key=f"{file_name}{extension}",
            Body=content,
            ContentType="text/plain",
        )
        return PutObjectResponse.from_response(response)

    except (BotoCoreError, ClientError):
        raise StorageError(f"Failed to upload file {file_name}")


def file_get_content(*, file_name: str) -> str:
    s3 = s3_get_client()
    credentials = s3_get_credentials()

    try:
        response = s3.get_object(Bucket=credentials.bucket_name, Key=file_name)
        return response["Body"].read().decode("utf-8")

    except (BotoCoreError, ClientError):
        raise StorageError(f"Failed to get file {file_name}")
