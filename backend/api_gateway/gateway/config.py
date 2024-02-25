from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 300

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret')
    JWT_COOKIE_SECURE = True
    JWT_TOKEN_LOCATION = ["cookies","headers"]
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 604800
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_ACCESS_CSRF_HEADER_NAME = 'X-CSRF-TOKEN-ACCESS'
    JWT_ACCESS_CSRF_FIELD_NAME = 'csrf_access_token'


class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    CACHE_REDIS_URL = 'redis://api-gateway-redis:6379/0'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', 'example')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    CACHE_REDIS_URL = 'redis://api-gateway-redis:6379/0'
