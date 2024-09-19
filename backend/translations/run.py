from translations.app import create_app
from translations.config.config import DEBUG_MODE, DevelopmentConfig, ProductionConfig


app = create_app(DevelopmentConfig if DEBUG_MODE else ProductionConfig)
