from tests.factories import TranslationFactory
from translations.services.dtos import ListTranslationDTO
from translations.db.entities import Translation
from datetime import datetime


class TestListTranslationDTO:
    simple_fields: dict[str, str | int | datetime] = {
        "original_title": "Origianal Title",
        "language": "en",
        "translator_id": 1,
        "requested_at": datetime.now(),
    }
    id_: int = 1
    status: Translation.StatusType = Translation.StatusType.RELEASED

    def test_to_dict(self) -> None:
        dto = ListTranslationDTO(id_=self.id_, status=self.status, **self.simple_fields)

        result = dto.to_dict()

        assert self.simple_fields.items() < result.items()
        assert self.id_ == result["id"]
        assert self.status.value == result["status"]

    def test_from_entity(self) -> None:
        translation = TranslationFactory()

        result = ListTranslationDTO.from_entity(translation)

        assert translation.id == result.id_
        assert translation.article.title == result.original_title
        assert translation.language.name == result.language
        assert translation.status == result.status
