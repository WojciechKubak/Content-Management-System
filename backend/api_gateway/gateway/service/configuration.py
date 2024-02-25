from gateway.service.auth import AuthService
from gateway.service.user import UserService
from gateway.service.article import ArticleService
from gateway.settings import USERS_URL, ARTICLES_URL

auth_service = AuthService(USERS_URL)
user_service = UserService(USERS_URL)
article_service = ArticleService(ARTICLES_URL)
