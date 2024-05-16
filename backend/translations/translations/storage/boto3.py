from dataclasses import dataclass
import boto3
import uuid


@dataclass
class Boto3Service:
    """
    A service class for interacting with AWS S3 using Boto3.

    Attributes:
        access_key_id (str): The AWS access key ID.
        secret_access_key (str): The AWS secret access key.
        bucket_name (str): The name of the S3 bucket.
    """

    access_key_id: str
    secret_access_key: str
    bucket_name: str

    def __post_init__(self):
        """Initializes the Boto3Service with the provided AWS credentials."""
        self.s3 = boto3.client('s3',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )

    def upload_to_txt_file(self, content: str, subfolder_name: str) -> str:
        """
        Uploads content to a new .txt file in a specified subfolder of the S3 bucket.

        Args:
            content (str): The content to be written to the file.
            subfolder_name (str): The name of the subfolder in the S3 bucket.

        Returns:
            str: The path of the newly created file in the S3 bucket.
        """
        file_path = f"{subfolder_name}/{uuid.uuid4().hex}.txt"
        self.s3.put_object(
            Body=content,
            Bucket=self.bucket_name,
            Key=file_path
        )
        return file_path

    def update_file_content(self, file_path: str, new_content: str) -> None:
        """
        Updates the content of a file in the S3 bucket.

        Args:
            file_path (str): The path of the file in the S3 bucket.
            new_content (str): The new content to be written to the file.
        """
        self.s3.put_object(
            Body=new_content,
            Bucket=self.bucket_name,
            Key=file_path
        )

    def delete_file(self, file_path: str) -> None:
        """
        Deletes a file from the S3 bucket.

        Args:
            file_path (str): The path of the file in the S3 bucket.
        """
        self.s3.delete_object(
            Bucket=self.bucket_name,
            Key=file_path
        )
    
    def read_file_content(self, file_path: str) -> str:
        """
        Reads the content of a file from the S3 bucket.

        Args:
            file_path (str): The path of the file in the S3 bucket.

        Returns:
            str: The content of the file.
        """
        response = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=file_path
        )
        return response['Body'].read().decode('utf-8')
