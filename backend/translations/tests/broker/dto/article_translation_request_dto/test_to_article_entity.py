from tests.factory import ArticleTranslationRequestDTOFactory


def test_to_article_entity() -> None:
    dto = ArticleTranslationRequestDTOFactory()

    result = dto.to_article_entity()
    
    assert dto.id_ == result.id
    assert dto.title == result.title
    assert dto.content_path == result.content_path
