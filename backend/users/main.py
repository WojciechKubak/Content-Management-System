from users.env_config import DEBUG_MODE
from users.config import DevelopmentConfig, ProductionConfig
from users.app import create_app


app = create_app(DevelopmentConfig if DEBUG_MODE else ProductionConfig)
