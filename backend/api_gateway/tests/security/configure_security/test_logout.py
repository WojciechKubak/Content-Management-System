from flask.testing import FlaskClient


def test_logout(client: FlaskClient) -> None:
    client.set_cookie('access_token_cookie', 'access_token')
    client.set_cookie('refresh_token_cookie', 'refresh_token')
    
    response = client.post('/logout')
    
    assert 200 == response.status_code
    assert b'Logout successful' in response.data

    assert not client.get_cookie('access_token_cookie')
    assert not client.get_cookie('refresh_token_cookie')
