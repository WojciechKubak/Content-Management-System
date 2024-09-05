from tests.factory import LanguageFactory
from translations.persistance.repository import LanguageRepository


def test_find_all(language_repository: LanguageRepository) -> None:
    languages = LanguageFactory.create_batch(5)
    result = language_repository.find_all()
    assert languages == result
