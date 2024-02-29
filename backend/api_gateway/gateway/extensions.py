from flask_jwt_extended import JWTManager
from flask_caching import Cache

# Extensions that are initialized in app factory
jwt_manager = JWTManager()
cache = Cache()
