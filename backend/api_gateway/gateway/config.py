from dotenv import load_dotenv
import json
import os

load_dotenv()

with open(os.environ.get('SERVICES_INDEX_JSON_PATH', 'gateway/config.py'), 'r') as json_data:
    services = json.load(json_data)

redis_config = {
    "CACHE_TYPE":  os.environ.get('CACHE_TYPE', 'simple'),
    "CACHE_REDIS_URL":  os.environ.get('CACHE_REDIS_URL', 'redis://api-gateway-redis:6379/0'),
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
}
