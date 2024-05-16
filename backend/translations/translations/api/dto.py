from translations.persistance.entity import StatusType, Translation
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Any


@dataclass
class TranslationDTO:
    """
    A data transfer object (DTO) that represents a translation.

    Attributes:
        id_ (int): The id of the translation.
        original_title (str): The original title of the translation.
        original_content (str): The original content of the translation.
        translation_title (str | None): The translated title.
        translation_content (str | None): The translated content.
        language (str): The language of the translation.
        status (StatusType): The status of the translation.
    """

    id_: int
    original_title: str
    original_content: str
    translation_title: str | None
    translation_content: str | None
    language: str
    status: StatusType

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the TranslationDTO to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the TranslationDTO.
        """
        return {
            'id': self.id_,
            'original_title': self.original_title,
            'original_content': self.original_content,
            'translation_title': self.translation_title,
            'translation_content': self.translation_content,
            'language': self.language,
            'status': self.status.value
        }

    def with_contents(self, original_content: str, translation_content: str) -> Self:
        """
        Returns a new TranslationDTO with updated original and translated contents.

        Args:
            original_content (str): The new original content.
            translation_content (str): The new translated content.

        Returns:
            TranslationDTO: A new TranslationDTO with the updated contents.
        """
        return self.__class__(
            id_=self.id_,
            original_title=self.original_title,
            original_content=original_content,
            translation_title=self.translation_title,
            translation_content=translation_content,
            language=self.language,
            status=self.status,
        )

    @classmethod
    def from_entity(cls, translation: Translation) -> Self:
        """
        Creates a new TranslationDTO from a Translation entity.

        This class method takes a Translation entity as an argument and returns a new instance of TranslationDTO
        with the corresponding attributes.

        Args:
            translation (Translation): The Translation entity.

        Returns:
            TranslationDTO: A new TranslationDTO created from the Translation entity.
        """
        return cls(
            id_=translation.id,
            original_title=translation.article.title,
            original_content=translation.article.content_path,
            translation_title=translation.title,
            translation_content=translation.content_path,
            language=translation.language.name,
            status=translation.status,
        )


@dataclass
class ListTranslationDTO:
    """
    A data transfer object (DTO) that represents a list of translations.

    Attributes:
        id_ (int): The id of the translation.
        original_title (str): The original title of the translation.
        language (str): The language of the translation.
        status (StatusType): The status of the translation.
        translator_id (int | None): The id of the translator. None if the translation is not yet assigned.
        requested_at (datetime): The time when the translation was requested.
    """
    id_: int
    original_title: str
    language: str
    status: StatusType
    translator_id: int | None
    requested_at: datetime

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the ListTranslationDTO to a dictionary.

        Returns:
            dict[str, Any]: A dictionary representation of the ListTranslationDTO.
        """
        return {
            'id': self.id_,
            'original_title': self.original_title,
            'language': self.language,
            'status': self.status.value,
            'translator_id': self.translator_id,
            'requested_at': self.requested_at
        }

    @classmethod
    def from_entity(cls, entity: Translation) -> Self:
        """
        Creates a new ListTranslationDTO from a Translation entity.

        Args:
            entity (Translation): The Translation entity.

        Returns:
            ListTranslationDTO: A new ListTranslationDTO created from the Translation entity.
        """
        return cls(
            id_=entity.id,
            original_title=entity.article.title,
            language=entity.language.name,
            status=entity.status,
            translator_id=entity.translator_id,
            requested_at=entity.requested_at
        )
