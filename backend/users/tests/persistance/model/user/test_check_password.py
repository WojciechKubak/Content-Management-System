from tests.factory import UserFactory


class TestCheckPassword:

    def test_when_incorrect(self) -> None:
        user = UserFactory()
        result = user.check_password('incorrect_password')
        assert not result

    def test_when_correct(self) -> None:
        user = UserFactory()
        result = user.check_password('password')
        assert result
