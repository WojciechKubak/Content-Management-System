from translations.persistance.entity import Article, Language, Translation
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Any
from enum import Enum


class LanguageEventType(Enum):
    """An enumeration representing the types of events that can occur to a Language."""
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


@dataclass
class LanguageEventDTO:
    """
    A data transfer object representing a Language event.

    Attributes:
        id_ (int): The ID of the Language.
        name (str): The name of the Language.
        code (str): The code of the Language.
        event_type (LanguageEventType): The type of the event.
    """

    id_: int
    name: str
    code: str
    event_type: LanguageEventType

    def to_entity(self) -> Language:
        """
        Converts the DTO to a Language entity.

        Returns:
            Language: The converted Language entity.
        """
        return Language(
            id=self.id_,
            name=self.name,
            code=self.code
        )

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> Self:
        """
        Creates a LanguageEventDTO from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary to convert.

        Returns:
            LanguageEventDTO: The created LanguageEventDTO.
        """
        return cls(
            id_=data['id'],
            name=data['name'],
            code=data['code'],
            event_type=LanguageEventType(data['event_type'].upper())
        )


@dataclass
class ArticleTranslationRequestDTO:
    """
    A data transfer object representing a request for an Article translation.

    Attributes:
        id_ (int): The ID of the Article.
        title (str): The title of the Article.
        content_path (str): The path to the content of the Article.
        language_id (int): The ID of the Language to translate to.
        date (datetime): The date of the request.
    """

    id_: int
    title: str
    content_path: str
    language_id: int
    date: datetime

    def to_article_entity(self) -> Article:
        """
        Converts the DTO to an Article entity.

        Returns:
            Article: The converted Article entity.
        """
        return Article(
            id=self.id_,
            title=self.title,
            content_path=self.content_path
        )
    
    def to_translation_entity(self) -> Translation:
        """
        Converts the DTO to a Translation entity.

        Returns:
            Translation: The converted Translation entity.
        """
        return Translation(
            article_id=self.id_,
            requested_at=self.date,
            language_id=self.language_id
        )
    
    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> Self:
        """
        Creates an ArticleTranslationRequestDTO from a dictionary.

        Args:
            data (dict[str, Any]): The dictionary to convert.

        Returns:
            ArticleTranslationRequestDTO: The created ArticleTranslationRequestDTO.
        """
        return cls(
            id_=data['id'],
            title=data['title'],
            content_path=data['content_path'],
            language_id=data['language_id'],
            date=data['date']
        )


@dataclass
class ArticleTranslationDTO:
    """
    A data transfer object representing an Article translation.

    Attributes:
        id_ (int): The ID of the Article.
        language_id (int): The ID of the Language the Article is translated to.
        title (str): The title of the Article.
        content_path (str): The path to the content of the Article.
        translator_id (int): The ID of the Translator.
    """

    id_: int
    language_id: int
    title: str
    content_path: str
    translator_id: int

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the DTO to a dictionary.

        Returns:
            dict[str, Any]: The converted dictionary.
        """
        return {
            'id': self.id_,
            'language_id': self.language_id,
            'title': self.title,
            'content_path': self.content_path,
            'translator_id': self.translator_id
        }

    @classmethod
    def from_entity(cls, entity: Translation) -> Self:
        """
        Creates an ArticleTranslationDTO from a Translation entity.

        Args:
            entity (Translation): The Translation entity to convert.

        Returns:
            ArticleTranslationDTO: The created ArticleTranslationDTO.
        """
        return cls(
            id_=entity.article_id,
            language_id=entity.language_id,
            title=entity.title,
            content_path=entity.content_path,
            translator_id=entity.translator_id
        )
