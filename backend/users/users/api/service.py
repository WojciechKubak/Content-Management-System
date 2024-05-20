from users.api.exceptions import (
    UserNotFoundException, 
    CommentNotFoundException,
    UserNameInUseException,
    EmailInUseException,
    UserNotFoundException,
    UserAlreadyActiveException,
    IncorrectPasswordException,
    UserNotActiveException
)
from users.email.configuration import mail
from users.persistance.entity import Comment, User
from dataclasses import dataclass
from typing import Any


@dataclass
class CommentService:
    """Service class for handling operations related to comments."""

    def add_comment(self, data: dict[str, Any]) -> Comment:
        """
        Add a new comment based on the provided data.

        Args:
            data (dict[str, Any]): Data for creating the new comment.

        Returns:
            Comment: The created comment.
        """
        if not User.find_by_id(data.get('user_id')):
            raise UserNotFoundException()
        comment = Comment.from_dict(data)
        comment.add()
        return comment

    def update_comment_content(self, data: dict[str, Any]) -> Comment:
        """
        Update the content of a comment based on the provided data.

        Args:
            data (dict[str, Any]): Data for updating the comment content.

        Returns:
            Comment: The updated comment.
        """
        result = Comment.find_by_id(data.get('id'))
        if not result:
            raise CommentNotFoundException()
        comment = Comment.from_dict(data)
        comment.update()
        return comment

    def delete_comment(self, id_: int) -> int:
        """
        Delete a comment by its ID.

        Args:
            id_ (int): The ID of the comment to delete.

        Returns:
            int: The ID of the deleted comment.
        """
        result = Comment.find_by_id(id_)
        if not result:
            raise CommentNotFoundException()
        result.delete()
        return result.id

    def get_comment_by_id(self, id_: int) -> Comment:
        """
        Get a comment by its ID.

        Args:
            id_ (int): The ID of the comment to retrieve.

        Returns:
            Comment: The retrieved comment.
        """
        result = Comment.find_by_id(id_)
        if not result:
            raise CommentNotFoundException()
        return result

    def get_user_comments(self, user_id: int) -> list[Comment]:
        """
        Get all comments for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[Comment]: List of comments for the specified user.
        """
        if not User.find_by_id(user_id):
            raise UserNotFoundException()
        return Comment.query.filter_by(user_id=user_id).all()

    def get_article_comments(self, article_id: int) -> list[Comment]:
        """
        Get all comments for a specific article.

        Args:
            article_id (int): The ID of the article.

        Returns:
            list[Comment]: List of comments for the specified article.
        """
        return Comment.query.filter_by(article_id=article_id).all()


@dataclass
class UserService:
    """Service class for handling operations related to users."""

    def add_user(self, data: dict[str, Any]) -> User:
        """
        Add a new user based on the provided data.

        Args:
            data (dict[str, Any]): Data for creating the new user.

        Returns:
            User: The created user.
        """
        if User.find_by_username(data.get('username')):
            raise UserNameInUseException()
        if User.find_by_email(data.get('email')):
            raise EmailInUseException()
        user = User.from_dict(data)
        user.add()
        return user

    def update_user(self, data: dict[str, Any]) -> User:
        """
        Update a user based on the provided data.

        Args:
            data (dict[str, Any]): Data for updating the user.

        Returns:
            User: The updated user.
        """
        result = User.find_by_id(data.pop('id'))
        if not result:
            raise UserNotFoundException()
        filtered_data = {key: val for key, val in data.items() if val}
        user = User.from_dict(result.to_dict() | filtered_data)
        user.update()
        return user

    def delete_user(self, id_: str) -> int:
        """
        Delete a user by their ID.

        Args:
            id_ (str): The ID of the user to delete.

        Returns:
            int: The ID of the deleted user.
        """
        result = User.find_by_id(id_)
        if not result:
            raise UserNotFoundException()
        result.delete()
        return result.id

    def get_user_by_name(self, username: str) -> User:
        """
        Get a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The retrieved user.
        """
        result = User.find_by_username(username)
        if not result:
            raise UserNotFoundException()
        return result

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The retrieved user.
        """
        result = User.find_by_email(email)
        if not result:
            raise UserNotFoundException()
        return result

    def get_user_by_id(self, id_: int) -> User:
        """
        Get a user by their ID.

        Args:
            id_ (int): The ID of the user.

        Returns:
            User: The retrieved user.
        """
        result = User.find_by_id(id_)
        if not result:
            raise UserNotFoundException()
        return result

    def get_all_users(self) -> list[User]:
        """
        Get a list of all users.

        Returns:
            list[User]: List of all users.
        """
        return User.query.all()

    def activate_user(self, id_: int) -> User:
        """
        Activate a user by their ID.

        Args:
            id_ (int): The ID of the user to activate.

        Returns:
            User: The activated user.
        """
        result = User.find_by_id(id_)
        if not result:
            raise UserNotFoundException()
        if result.is_active:
            raise UserAlreadyActiveException()
        result.set_active()
        return result

    def check_login_credentials(self, username: str, password: str) -> User:
        """
        Check login credentials and return the user.

        Args:
            username (str): The username of the user.
            password (str): The password for login.

        Returns:
            User: The authenticated user.
        """
        result = User.find_by_username(username)
        if not result:
            raise UserNotFoundException()
        if not result.check_password(password):
            raise IncorrectPasswordException()
        if not result.is_active:
            raise UserNotActiveException()
        return result

    def register_user(self, data: dict[str, Any]) -> User:
        """
        Register a new user based on the provided data and send an activation email.

        Args:
            data (dict[str, Any]): Data for creating the new user.

        Returns:
            User: The created user.
        """
        if User.find_by_username(data.get('username')):
            raise UserNameInUseException()
        if User.find_by_email(data.get('email')):
            raise EmailInUseException()
        user = User.from_dict(data)
        user.add()
        mail.send_activation_mail(user.id, user.email)
        return user
