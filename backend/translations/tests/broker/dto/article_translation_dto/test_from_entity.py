from tests.factory import TranslationFactory
from translations.broker.dto import ArticleTranslationDTO


def test_from_entity() -> None:
    translation = TranslationFactory()

    result = ArticleTranslationDTO.from_entity(translation)

    assert translation.article_id == result.id_
    assert translation.language_id == result.language_id
    assert translation.translator_id == result.translator_id
