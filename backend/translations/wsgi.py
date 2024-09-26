from translations.config.environments import base, production
from translations.config.environments.base import DEBUG
from translations.app import create_app


app = create_app(base if DEBUG else production)
