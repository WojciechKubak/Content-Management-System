from dotenv import load_dotenv
import json
import os

load_dotenv()

with open(os.environ.get('SERVICES_INDEX_JSON_PATH', 'gateway/config.py'), 'r') as json_data:
    services = json.load(json_data)
