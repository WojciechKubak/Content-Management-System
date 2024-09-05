

def test_upload_to_txt_file(conn, service, bucket_name: str) -> None:
    file_content = 'Hello, World!'
    result = service.upload_to_txt_file(file_content, 'subfolder')
    expected = conn.Object(bucket_name, result).get()['Body'].read().decode('utf-8')
    assert expected == file_content
