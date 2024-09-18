from translations.config.config import DevelopmentConfig, ProductionConfig
from translations.env_config import DEBUG_MODE
from translations.app import create_app


app = create_app(DevelopmentConfig if DEBUG_MODE else ProductionConfig)
