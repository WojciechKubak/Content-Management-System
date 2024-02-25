from gateway.service.auth import AuthService
from gateway.service.user import UserService
from gateway.service.article import ArticleService
from gateway.config import security_config, USERS_URL, ARTICLES_URL

auth_service = AuthService(security_config)

user_service = UserService(USERS_URL)
article_service = ArticleService(ARTICLES_URL)
