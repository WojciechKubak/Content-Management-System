from tests.factory import TranslationFactory
from translations.persistance.repository import TranslationRepository
from translations.persistance.entity import StatusType


def test_find_by_status(translation_repository: TranslationRepository) -> None:
    translations = TranslationFactory.create_batch(5, status=StatusType.REQUESTED)
    result = translation_repository.find_by_status(StatusType.REQUESTED)
    assert translations == result
