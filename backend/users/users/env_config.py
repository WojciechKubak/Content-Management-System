from dotenv import load_dotenv
import os


load_dotenv()

DEBUG_MODE = int(os.environ.get('DEBUG', 1))

REGISTER_TOKEN_LIFESPAN = int(os.environ.get('REGISTER_TOKEN_LIFESPAN', 3600000))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
BASE_URL = os.environ.get('BASE_URL', 'localhost.localdomain')
TEMPLATE_MODULE = os.environ.get('TEMPLATE_MODULE', 'users.email')
