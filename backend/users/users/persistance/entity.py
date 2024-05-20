from users.persistance.configuration import sa
from sqlalchemy import Integer, String, Boolean, func, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Self, Any
from datetime import datetime
from enum import Enum


class UserRoles(Enum):
    """An enumeration representing the status of a translation."""

    USER = 'USER'
    REDACTOR = 'REDACTOR'
    TRANSLATOR = 'TRANSLATOR'
    ADMIN = 'ADMIN'


class User(sa.Model):
    """
    SQLAlchemy model representing the 'users' table.

    Attributes:
        id (int): Primary key for the user.
        username (str): User's username.
        email (str): User's email address.
        password (str): Hashed password using bcrypt.
        is_active (bool): Flag indicating whether the user is active or not.
        role (UserRole): User's role, chosen from the predefined set of roles.
        created_at (datetime): Timestamp indicating when the user was created.
        updated_at (datetime): Timestamp indicating the last update to the user.
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRoles] = mapped_column(
        SQLAlchemyEnum(UserRoles), default=UserRoles.USER)

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the User instance to a JSON-compatible dictionary.

        Returns:
            dict[str, Any]: JSON-compatible dictionary representing the User instance.
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'is_active': self.is_active,
        }

    def add(self) -> None:
        """Add the User instance to the session and commit the changes."""
        sa.session.add(self)
        sa.session.commit()

    def update(self) -> None:
        """Merge and update the User instance in the session and commit the changes."""
        updated = sa.session.merge(self)
        sa.session.add(updated)
        sa.session.commit()

    def delete(self) -> None:
        """Delete the User instance from the session and commit the changes."""
        sa.session.delete(self)
        sa.session.commit()

    def set_active(self) -> None:
        """Set the user's 'is_active' flag to True and commit the changes."""
        self.is_active = True
        sa.session.commit()

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the hashed password of the user.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        """
        Find a User instance by ID.

        Args:
            id_ (int): The ID to search for.

        Returns:
            User | None: The found User instance or None if not found.
        """
        return sa.session.query(User).filter_by(id=id_).first()

    @classmethod
    def find_by_username(cls, username: str) -> Self | None:
        """
        Find a User instance by username.

        Args:
            username (str): The username to search for.

        Returns:
            User | None: The found User instance or None if not found.
        """
        return sa.session.query(User).filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> Self | None:
        """
        Find a User instance by email address.

        Args:
            email (str): The email address to search for.

        Returns:
            User | None: The found User instance or None if not found.
        """
        return sa.session.query(User).filter_by(email=email).first()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a User instance from a JSON-compatible dictionary.

        Args:
            data (dict[str, Any]): JSON-compatible dictionary representing the User instance.

        Returns:
            User: The created User instance.
        """
        hashed_passowrd = generate_password_hash(data.get('password'))
        return User(**data | {'password': hashed_passowrd})


class Comment(sa.Model):
    """
    Comment Class

    A SQLAlchemy Model class for the 'comments' table.

    Attributes:
        id (int): Primary key column representing the comment ID.
        content (str): Column representing the content of the comment.
        article_id (int): Column representing the ID of the associated article.
        user_id (int): Column representing the ID of the user who created the comment.
        created_at (datetime): Column representing the creation timestamp of the comment.
        updated_at (datetime): Column representing the last update timestamp of the comment.
    """
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    content: Mapped[str] = mapped_column(String(1000))
    article_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey('users.id'))

    created_at: Mapped[datetime] = mapped_column(insert_default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the Comment instance to a JSON-compatible dictionary.

        Returns:
            dict[str, Any]: JSON-compatible dictionary representing the Comment instance.
        """
        return {
            'id': self.id,
            'content': self.content,
            'article_id': self.article_id,
            'user_id': self.user_id,
        }

    def add(self) -> None:
        """Add the Comment instance to the session and commit the changes."""
        sa.session.add(self)
        sa.session.commit()

    def update(self) -> None:
        """Merge and update the Comment instance in the session and commit the changes."""
        updated = sa.session.merge(self)
        sa.session.add(updated)
        sa.session.commit()

    def delete(self) -> None:
        """Delete the Comment instance from the session and commit the changes."""
        sa.session.delete(self)
        sa.session.commit()

    @classmethod
    def find_by_id(cls, id_: int) -> Self | None:
        """
        Find a Comment instance by ID.

        Args:
            id_ (int): The ID to search for.

        Returns:
            Comment | None: The found Comment instance or None if not found.
        """
        return sa.session.query(Comment).filter_by(id=id_).first()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """
        Create a Comment instance from a JSON-compatible dictionary.

        Args:
            data (dict[str, Any]): JSON-compatible dictionary representing the Comment instance.

        Returns:
            Comment: The created Comment instance.
        """
        return Comment(**data)
