from gateway.security.role_auth import requires_roles, requires_no_jwt
from flask import Flask, Response, make_response
import pytest 


@pytest.fixture(scope='function', autouse=True)
def register_resources(app: Flask):

    @app.get('/protected')
    @requires_roles(['admin'])
    def resource_1() -> Response:
        return make_response({'message': 'Resource accessed successfully'}, 200)
    
    @app.get('/exposed')
    @requires_no_jwt()
    def resource_2() -> Response:
        return make_response({'message': 'Resource accessed successfully'}, 200)
