from gateway.config import DevelopmentConfig, ProductionConfig
from gateway import create_app
import os

debug_mode = os.environ.get('DEBUG', 1)
app = create_app(DevelopmentConfig if debug_mode else ProductionConfig)
