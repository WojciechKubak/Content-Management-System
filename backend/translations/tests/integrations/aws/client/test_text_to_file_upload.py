from translations.integrations.aws.client import (
    text_to_file_upload,
    PutObjectResponse,
    StorageError,
)
from botocore.exceptions import BotoCoreError, ClientError
from unittest.mock import MagicMock
import pytest


def test_text_to_file_upload_success(mock_boto3_client) -> None:
    mock_s3 = MagicMock()

    mock_response = MagicMock()
    mock_response.ETag = '"test_etag"'
    mock_response.ServerSideEncryption = "AES256"

    mock_s3.put_object.return_value = mock_response
    mock_boto3_client.return_value = mock_s3

    result = text_to_file_upload(file_name="test_file", content="test content")

    mock_s3.put_object.assert_called_once_with(
        Bucket="test_bucket_name",
        Key="test_file.txt",
        Body="test content",
        ContentType="text/plain",
    )
    assert PutObjectResponse.from_response(mock_response) == result


def test_text_to_file_upload_failure(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_s3.put_object.side_effect = ClientError({"Error": {}}, "put_object")
    mock_boto3_client.return_value = mock_s3

    with pytest.raises(StorageError, match="Failed to upload file test_file.txt"):
        text_to_file_upload(file_name="test_file.txt", content="test content")


def test_text_to_file_upload_boto_core_error(mock_boto3_client) -> None:
    mock_s3 = MagicMock()
    mock_s3.put_object.side_effect = BotoCoreError
    mock_boto3_client.return_value = mock_s3

    with pytest.raises(StorageError, match="Failed to upload file test_file.txt"):
        text_to_file_upload(file_name="test_file.txt", content="test content")
