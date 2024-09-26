from tests.factories import TranslationFactory
from translations.services.dtos import TranslationDTO
from translations.db.entities import Translation


class TestTranslationDTO:
    simple_fields: dict[str, str] = {
        "original_title": "Original Title",
        "original_content": "Original Content",
        "translation_title": "Translated Title",
        "translation_content": "Translated Content",
        "language": "en",
    }
    id_: int = 1
    status: Translation.StatusType = Translation.StatusType.RELEASED

    def test_to_dict(self) -> None:
        dto = TranslationDTO(id_=self.id_, status=self.status, **self.simple_fields)

        result = dto.to_dict()

        assert self.simple_fields.items() < result.items()
        assert self.id_ == result["id"]
        assert self.status.value == result["status"]

    def test_with_contents(self) -> None:
        dto = TranslationDTO(id_=self.id_, status=self.status, **self.simple_fields)

        original_content: str = "original"
        translation_content: str = "translation"

        result = dto.with_contents(original_content, translation_content)

        assert original_content == result.original_content
        assert translation_content == result.translation_content

    def test_from_entity(self) -> None:
        translation = TranslationFactory()

        result = TranslationDTO.from_entity(translation)

        assert translation.id == result.id_
        assert translation.article.title == result.original_title
        assert translation.article.content_path == result.original_content
        assert translation.content_path == result.translation_content
        assert translation.language.name == result.language
        assert translation.status == result.status
