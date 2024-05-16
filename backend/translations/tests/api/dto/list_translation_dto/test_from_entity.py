from tests.factory import TranslationFactory
from translations.api.dto import ListTranslationDTO


def test_from_entity() -> None:
    translation = TranslationFactory()
    result = ListTranslationDTO.from_entity(translation)

    assert translation.id == result.id_
    assert translation.article.title == result.original_title
    assert translation.language.name == result.language
