from translations.persistance.entity import Article, Translation
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Any


@dataclass
class ArticleTranslationRequestDTO:
    id_: int
    title: str
    content_path: str
    language_id: int
    date: datetime

    def to_article_entity(self) -> Article:
        return Article(id=self.id_, title=self.title, content_path=self.content_path)

    def to_translation_entity(self) -> Translation:
        return Translation(
            article_id=self.id_, requested_at=self.date, language_id=self.language_id
        )

    @classmethod
    def from_dto(cls, data: dict[str, Any]) -> Self:
        return cls(
            id_=data["id"],
            title=data["title"],
            content_path=data["content_path"],
            language_id=data["language_id"],
            date=data["date"],
        )


@dataclass
class ArticleTranslationDTO:
    id_: int
    language_id: int
    title: str
    content_path: str
    translator_id: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id_,
            "language_id": self.language_id,
            "title": self.title,
            "content_path": self.content_path,
            "translator_id": self.translator_id,
        }

    @classmethod
    def from_entity(cls, entity: Translation) -> Self:
        return cls(
            id_=entity.article_id,
            language_id=entity.language_id,
            title=entity.title,
            content_path=entity.content_path,
            translator_id=entity.translator_id,
        )
