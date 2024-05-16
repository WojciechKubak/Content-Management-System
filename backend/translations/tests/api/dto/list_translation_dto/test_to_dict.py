from translations.api.dto import ListTranslationDTO
from translations.persistance.entity import StatusType


def test_to_dict() -> None:
    data = {
        'id_': 1,
        'original_title': 'title',
        'language': 'language',
        'status': StatusType.PENDING,
        'translator_id': 1,
        'requested_at': '2021-01-01 00:00:00'
    }
    result = ListTranslationDTO(**data).to_dict()

    assert data['id_'] == result['id']
    assert data['original_title'] == result['original_title']
    assert data['status'].value == result['status']
