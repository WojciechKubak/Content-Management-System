from translations.broker.dto import ArticleTranslationRequestDTO
from datetime import datetime


def test_from_dto() -> None:
    data = {
        'id': 1,
        'title': 'title',
        'content_path': 'path/to/content',
        'language_id': 1,
        'date': datetime.now()
    }

    result = ArticleTranslationRequestDTO.from_dto(data)
    
    assert data['id'] == result.id_
    assert  data['title'] == result.title
    assert data['language_id'] == result.language_id
