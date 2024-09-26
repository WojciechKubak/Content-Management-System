from translations.db.entities import Translation
from dataclasses import dataclass
from typing import Self, Any


@dataclass
class TranslationFilters:
    status: Translation.StatusType | None
    language_id: int | None
    article_id: int | None
    translator_id: int | None

    @classmethod
    def from_query_params(cls, query_params: dict[str, Any]) -> Self:
        return cls(
            status=query_params.get("status"),
            language_id=query_params.get("language_id"),
            article_id=query_params.get("article_id"),
            translator_id=query_params.get("translator_id"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}
