from users.email.configuration import MailConfig
from flask_sqlalchemy import SQLAlchemy

# Extensions that are initialized in app factory
sa = SQLAlchemy()
mail_config = MailConfig()
