from users.env_config import (
    REGISTER_TOKEN_LIFESPAN, 
    MAIL_USERNAME, 
    BASE_URL, 
    TEMPLATE_MODULE
)
from users.email.service import MailService


mail = MailService(REGISTER_TOKEN_LIFESPAN, MAIL_USERNAME, BASE_URL, TEMPLATE_MODULE)
