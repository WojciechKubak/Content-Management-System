from translations.persistance.entity import StatusType, Language, Translation, Article
from translations.persistance.configuration import sa
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from abc import ABC, abstractmethod

    
@dataclass
class CrudRepository[T](ABC):
    """
    An abstract base class representing a CRUD repository.

    This class should be subclassed and its methods overridden to provide the
    functionality for a specific entity type.
    """

    @abstractmethod
    def save_or_update(self, entity: T) -> T:
        """
        Saves or updates an entity.

        Args:
            entity (T): The entity to save or update.

        Returns:
            T: The saved or updated entity.
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        """
        Finds an entity by its ID.

        Args:
            entity_id (int): The ID of the entity.

        Returns:
            T | None: The found entity, or None if no entity was found.
        """
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T]: A list of all entities.
        """
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        """
        Deletes an entity by its ID.

        Args:
            entity_id (int): The ID of the entity.
        """
        pass


@dataclass
class CrudRepositoryORM[T: sa.Model](CrudRepository[T]):
    """
    A concrete implementation of the CrudRepository abstract base class for SQLAlchemy models.

    Attributes:
        db (SQLAlchemy): The SQLAlchemy object.
    """

    db: SQLAlchemy

    def __post_init__(self):
        """Initializes the CrudRepositoryORM with the provided SQLAlchemy object."""
        self.sa = self.db
        self.entity = self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, entity: T) -> T:
        """
        Saves or updates an entity.

        Args:
            entity (T): The entity to save or update.

        Returns:
            T: The saved or updated entity.
        """
        self.sa.session.merge(entity)
        self.sa.session.commit()
        return entity

    def delete_by_id(self, id_: int) -> None:
        """
        Deletes an entity by its ID.

        Args:
            id_ (int): The ID of the entity.
        """
        entity = self.sa.session.query(self.entity).filter_by(id=id_).first()
        self.sa.session.delete(entity)
        self.sa.session.commit()

    def find_by_id(self, id_: int) -> T | None:
        """
        Finds an entity by its ID.

        Args:
            id_ (int): The ID of the entity.

        Returns:
            T: The found entity, or None if no entity was found.
        """
        return self.sa.session.query(self.entity).filter_by(id=id_).first()

    def find_all(self) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T]: A list of all entities.
        """
        return self.sa.session.query(self.entity).all()


@dataclass
class TranslationRepository(CrudRepositoryORM[Translation]):
    """A repository class for interacting with Translation entities."""

    def find_by_language(self, language_id: int) -> list[Translation]:
        """
        Retrieves all translations associated with a specific language.

        Args:
            language_id (int): The ID of the language.

        Returns:
            list[Translation]: A list of Translation objects associated with the language.
        """
        return self.sa.session.query(Translation).filter_by(language_id=language_id).all()

    def find_by_language_and_article(self, language_id: int, article_id: int) -> Translation:
        """
        Retrieves a translation associated with a specific language and article.

        Args:
            language_id (int): The ID of the language.
            article_id (int): The ID of the article.

        Returns:
            Translation: The Translation object associated with the language and article.
        """
        return self.sa.session.query(Translation).filter_by(language_id=language_id) \
            .filter_by(article_id=article_id).first()
    
    def find_by_status(self, status_type: StatusType) -> list[Translation]:
        """
        Retrieves all translations with a specific status.

        Args:
            status_type (StatusType): The status type.

        Returns:
            list[Translation]: A list of Translation objects with the specified status.
        """
        return self.sa.session.query(Translation).filter_by(status=status_type).all()


@dataclass
class LanguageRepository(CrudRepositoryORM[Language]):
    """A repository class for interacting with Language entities."""
    pass


@dataclass
class ArticleRepository(CrudRepositoryORM[Article]):
    """A repository class for interacting with Article entities."""
    pass


language_repository = LanguageRepository(sa)
translation_repository = TranslationRepository(sa)
article_repository = ArticleRepository(sa)
