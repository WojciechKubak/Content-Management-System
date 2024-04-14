from articles.config import DevelopmentConfig, ProductionConfig
from articles import create_app
from articles.settings import DEBUG_MODE


app = create_app(DevelopmentConfig if DEBUG_MODE else ProductionConfig)
