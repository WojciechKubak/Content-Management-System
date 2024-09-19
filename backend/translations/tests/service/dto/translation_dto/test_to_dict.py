from backend.translations.translations.services.dtos import TranslationDTO
from translations.persistance.entity import StatusType


def test_to_dict() -> None:
    data = {
        "id_": 1,
        "original_title": "title",
        "original_content": "content",
        "language": "language",
        "status": StatusType.PENDING,
        "translation_title": "translation_title",
        "translation_content": "translation_content",
    }
    result = TranslationDTO(**data).to_dict()

    assert data["id_"] == result["id"]
    assert data["original_title"] == result["original_title"]
    assert data["status"].value == result["status"]
