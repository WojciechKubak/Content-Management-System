from botocore.exceptions import ClientError
import pytest


def test_delete_file(conn, service, bucket_name: str) -> None:
    conn.Bucket(bucket_name).put_object(Key="myfile.txt", Body="Hello, World!")
    service.delete_file("myfile.txt")

    with pytest.raises(ClientError) as e:
        conn.Object(bucket_name, "myfile.txt").load()
    assert "not found" in str(e.value).lower()
