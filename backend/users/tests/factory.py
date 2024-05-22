from users.persistance.configuration import sa
from users.persistance.entity import Comment, User, UserRoleType
from factory import DictFactory, Sequence, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
from werkzeug.security import generate_password_hash
from datetime import datetime


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = sa.session
        sqlalchemy_session_persistence = 'commit'
        exclude = ('raw_password',)

    id = Sequence(lambda n: n + 1)
    username = Sequence(lambda n: f'user{n}')
    email = Sequence(lambda n: f'user{n}@example.com')
    password = LazyAttribute(lambda obj: generate_password_hash(obj.raw_password))
    raw_password = 'password'
    is_active = False
    role = UserRoleType.USER
    created_at = datetime.now()
    updated_at = datetime.now()


class CommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = sa.session
        sqlalchemy_session_persistence = 'commit'  

    id = Sequence(lambda n: n + 1)
    content = Sequence(lambda n: f'Comment content {n}')
    article_id = Sequence(lambda n: n + 1)
    user_id = Sequence(lambda n: n + 1)
    created_at = datetime.now()
    updated_at = datetime.now()


class UserDtoFactory(DictFactory):
    username = 'User'
    email = 'user@example.com'
    password = 'password'


class CommentDtoFactory(DictFactory):
    content = 'dummy content'
    article_id = Sequence(lambda n: n + 1)
    user_id = Sequence(lambda n: n + 1)
