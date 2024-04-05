import os

# Load aditional environment variables from .env file
REGISTER_TOKEN_LIFESPAN = int(os.environ.get('REGISTER_TOKEN_LIFESPAN', 3600000))
