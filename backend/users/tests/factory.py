from users.persistance.configuration import sa
, UserRoles
from users.persistance.entity import Comment, User
from factory import SubFactory, Sequence, PostGenerationMethodCall, post_generation
from factory.alchemy import SQLAlchemyModelFactory
from werkzeug.security import generate_password_hash
from datetime import datetime


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)
    username = Sequence(lambda n: f'user{n}')
    email = Sequence(lambda n: f'user{n}@example.com')
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = False
    role = UserRoles.USER
    created_at = datetime.now()
    updated_at = datetime.now()

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        self.password = generate_password_hash(extracted)


class CommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = sa.session

    id = Sequence(lambda n: n + 1)
    content = Sequence(lambda n: f'Comment content {n}')
    article_id = Sequence(lambda n: n)
    user = SubFactory(UserFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
