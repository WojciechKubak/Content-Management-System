
from users.persistance.entity import Comment, User
from users.persistance.configuration import sa
from typing import Any, Callable


class TestUserCrud:

    def test_add(self, user_model_with_id: Callable[[int], User]) -> None:
        new_id = 9999
        user_with_new_id = user_model_with_id(new_id)
        user_with_new_id.add()
        assert sa.session.query(User).filter_by(id=new_id).first()

    def test_update(self, user_model_data: dict[str, Any]) -> None:
        new_email = 'new@example.com'
        user_with_existing_id = User(**user_model_data | {'email': new_email})
        user_with_existing_id.update()
        expected = sa.session.query(User).filter_by(id=user_model_data['id']).first().email
        assert new_email == expected

    def test_delete(self, user_model: User) -> None:
        id_to_delete = user_model.id
        user_model.delete()
        assert not sa.session.query(User).filter_by(id=id_to_delete).first()

    def test_find_by_id(self, user_model: User) -> None:
        assert user_model == User.find_by_id(user_model.id)

    def test_find_by_username(self, user_model: User) -> None:
        assert user_model == User.find_by_username(user_model.username)

    def test_find_by_email(self, user_model: User) -> None:
        assert user_model == User.find_by_email(user_model.email)
