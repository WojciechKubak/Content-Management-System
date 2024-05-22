from users.api.service import CommentService
from tests.factory import CommentFactory, UserFactory


class TestGetArticleComments:

    def test_when_no_comments(self, comment_service: CommentService) -> None:
        result = comment_service.get_article_comments(999)
        assert not result

    def test_when_comments_found(self, comment_service: CommentService) -> None:
        user = UserFactory()
        comments = CommentFactory.create_batch(5, user_id=user.id, article_id=1)

        result = comment_service.get_article_comments(1)

        assert comments == result
