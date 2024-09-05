from tests.factory import ArticleTranslationRequestDTOFactory


def test_to_translation_entity() -> None:
    dto = ArticleTranslationRequestDTOFactory()

    result = dto.to_translation_entity()

    assert dto.id_ == result.article_id
    assert dto.language_id == result.language_id
    assert dto.date == result.requested_at
