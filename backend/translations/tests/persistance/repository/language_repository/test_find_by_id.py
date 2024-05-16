from tests.factory import LanguageFactory
from translations.persistance.repository import LanguageRepository


def test_find_by_id(language_repository: LanguageRepository) -> None:
    language = LanguageFactory()
    result = language_repository.find_by_id(language.id)
    assert language == result
