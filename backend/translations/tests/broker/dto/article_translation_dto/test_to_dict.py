from tests.factory import ArticleTranslationDTOFactory


def test_to_dict() -> None:
    dto = ArticleTranslationDTOFactory()

    result = dto.to_dict()

    assert dto.id_ == result['id']
    assert dto.language_id == result['language_id']
    assert dto.translator_id == result['translator_id']
