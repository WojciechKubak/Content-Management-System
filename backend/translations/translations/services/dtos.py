from translations.persistance.entity import StatusType, Translation
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Any


@dataclass
class TranslationDTO:
    id_: int
    original_title: str
    original_content: str
    translation_title: str | None
    translation_content: str | None
    language: str
    status: StatusType

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id_,
            "original_title": self.original_title,
            "original_content": self.original_content,
            "translation_title": self.translation_title,
            "translation_content": self.translation_content,
            "language": self.language,
            "status": self.status.value,
        }

    def with_contents(self, original_content: str, translation_content: str) -> Self:
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
    id_: int
    original_title: str
    language: str
    status: StatusType
    translator_id: int | None
    requested_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id_,
            "original_title": self.original_title,
            "language": self.language,
            "status": self.status.value,
            "translator_id": self.translator_id,
            "requested_at": self.requested_at,
        }

    @classmethod
    def from_entity(cls, entity: Translation) -> Self:
        return cls(
            id_=entity.id,
            original_title=entity.article.title,
            language=entity.language.name,
            status=entity.status,
            translator_id=entity.translator_id,
            requested_at=entity.requested_at,
        )
