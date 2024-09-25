from translations.db.entities import Language, Translation, Article
from translations.db.configuration import sa
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class CrudRepository[T](ABC):

    @abstractmethod
    def save_or_update(self, entity: T) -> T:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        pass


@dataclass
class CrudRepositoryORM[T: sa.Model](CrudRepository[T]):
    db: SQLAlchemy

    def __post_init__(self):
        self.sa = self.db
        self.entity = self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, entity: T) -> T:
        self.sa.session.merge(entity)
        self.sa.session.commit()
        return entity

    def delete_by_id(self, id_: int) -> None:
        entity = self.sa.session.query(self.entity).filter_by(id=id_).first()
        self.sa.session.delete(entity)
        self.sa.session.commit()

    def find_by_id(self, id_: int) -> T | None:
        return self.sa.session.query(self.entity).filter_by(id=id_).first()

    def find_all(self, limit: int, offset: int) -> list[T]:
        return self.sa.session.query(self.entity).offset(offset).limit(limit).all()


@dataclass
class TranslationRepository(CrudRepositoryORM[Translation]):

    def find_by_language(self, language_id: int) -> list[Translation]:
        return (
            self.sa.session.query(Translation).filter_by(language_id=language_id).all()
        )

    def find_by_language_and_article(
        self, language_id: int, article_id: int
    ) -> Translation:
        return (
            self.sa.session.query(Translation)
            .filter_by(language_id=language_id)
            .filter_by(article_id=article_id)
            .first()
        )

    def find_by_status(self, status_type: Translation.StatusType) -> list[Translation]:
        return self.sa.session.query(Translation).filter_by(status=status_type).all()


@dataclass
class LanguageRepository(CrudRepositoryORM[Language]):
    pass


@dataclass
class ArticleRepository(CrudRepositoryORM[Article]):
    pass


language_repository = LanguageRepository(sa)
translation_repository = TranslationRepository(sa)
article_repository = ArticleRepository(sa)
