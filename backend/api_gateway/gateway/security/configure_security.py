from gateway.security.role_auth import requires_no_jwt
from gateway.service.configuration import auth_service
from flask import Flask, Response, request, make_response
from flask_jwt_extended import (
    set_access_cookies, 
    set_refresh_cookies,
    unset_jwt_cookies,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)


def configure_security(app: Flask) -> None:

    @app.post('/login')
    @requires_no_jwt()
    def login() -> Response:
        data = request.get_json()
        username, password = data.get('username'), data.get('password')

        if not username or not password:
            return make_response({'message': 'No credentials provided'}, 400)

        if not (user_data := auth_service.verify_user_credentials(username, password)):
            return make_response({'message': 'Invalid credentials'}, 401)
        
        access_token = create_access_token(identity=user_data['id'])
        refresh_token = create_refresh_token(identity=user_data['id'])

        response = make_response({'message': "Login successful"})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        
        return response

    @app.post('/logout')
    def logout() -> Response:
        response = make_response({'message': "Logout successful"})
        unset_jwt_cookies(response)
        return response
    
    @app.post('/refresh')
    @jwt_required(refresh=True)
    def refresh() -> Response:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return make_response({'access_token': access_token})
