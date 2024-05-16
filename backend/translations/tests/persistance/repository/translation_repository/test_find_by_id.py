from tests.factory import TranslationFactory
from translations.persistance.repository import TranslationRepository


def test_find_by_id(translation_repository: TranslationRepository) -> None:
    translation = TranslationFactory()
    result = translation_repository.find_by_id(translation.id)
    assert translation == result
