from dotenv import load_dotenv
import os


load_dotenv()

DEBUG_MODE = int(os.environ.get('DEBUG', 1))

REGISTER_TOKEN_LIFESPAN_SECS = int(os.environ.get('REGISTER_TOKEN_LIFESPAN_SECS'))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
BASE_URL = os.environ.get('BASE_URL')
TEMPLATE_MODULE = os.environ.get('TEMPLATE_MODULE')