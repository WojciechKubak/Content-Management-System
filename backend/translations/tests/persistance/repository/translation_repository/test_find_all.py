from tests.factory import TranslationFactory
from translations.persistance.repository import TranslationRepository


def test_find_all(translation_repository: TranslationRepository) -> None:
    translations = TranslationFactory.create_batch(5)
    result = translation_repository.find_all()
    assert translations == result
