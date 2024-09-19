from tests.factory import TranslationFactory
from translations.services.dtos import TranslationDTO


def test_from_entity() -> None:
    translation = TranslationFactory()
    result = TranslationDTO.from_entity(translation)

    assert translation.id == result.id_
    assert translation.article.title == result.original_title
    assert translation.language.name == result.language
    assert translation.status == result.status
