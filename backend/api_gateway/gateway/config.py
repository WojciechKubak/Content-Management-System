from dotenv import load_dotenv
import ast
import os

load_dotenv()

USERS_URL = os.environ.get('USERS_URL')
ARTICLES_URL = os.environ.get('ARTICLES_URL')


redis_config = {
    "CACHE_TYPE":  os.environ.get('CACHE_TYPE', 'simple'),
    "CACHE_REDIS_URL":  os.environ.get('CACHE_REDIS_URL', 'redis://api-gateway-redis:6379/0'),
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
}

security_config = {
        'USERS_URL': os.environ.get('USERS_URL'),
        'JWT_COOKIE_SECURE': ast.literal_eval(os.environ.get('JWT_COOKIE_SECURE')),
        'JWT_TOKEN_LOCATION': ast.literal_eval(os.environ.get('JWT_TOKEN_LOCATION')),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY'),
        'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES')),
        'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES')),
        'JWT_COOKIE_CSRF_PROTECT': ast.literal_eval(os.environ.get('JWT_COOKIE_CSRF_PROTECT')),
        'JWT_ACCESS_COOKIE_NAME': os.environ.get('JWT_ACCESS_COOKIE_NAME'),
        'JWT_ACCESS_CSRF_HEADER_NAME': os.environ.get('JWT_ACCESS_CSRF_HEADER_NAME'),
        'JWT_ACCESS_CSRF_FIELD_NAME': os.environ.get('JWT_ACCESS_CSRF_FIELD_NAME'),
        'JWT_HEADER_NAME': os.environ.get('JWT_HEADER_NAME'),
        'JWT_HEADER_TYPE': os.environ.get('JWT_HEADER_TYPE'),
    }
