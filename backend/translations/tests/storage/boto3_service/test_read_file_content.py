

def test_read_file_content(conn, service, bucket_name: str) -> None:
    file_content = 'Hello, World!'
    conn.Bucket(bucket_name).put_object(Key='myfile.txt', Body=file_content)
    assert file_content == service.read_file_content('myfile.txt')
