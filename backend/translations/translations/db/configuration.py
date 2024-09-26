from translations.common.models import BaseModel
from flask_sqlalchemy import SQLAlchemy


sa = SQLAlchemy(model_class=BaseModel)
