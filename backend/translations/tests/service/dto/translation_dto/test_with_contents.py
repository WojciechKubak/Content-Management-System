from backend.translations.translations.services.dtos import TranslationDTO
from translations.persistance.entity import StatusType


def test_with_contents() -> None:
    data = {
        "id_": 1,
        "original_title": "title",
        "original_content": "content",
        "language": "language",
        "status": StatusType.PENDING,
        "translation_title": "translation_title",
        "translation_content": "translation_content",
    }
    result = TranslationDTO(**data).with_contents(
        f"new_{data['original_content']}",
        f"new_{data['translation_content']}",
    )

    assert f"new_{data['original_content']}" == result.original_content
    assert f"new_{data['translation_content']}" == result.translation_content
