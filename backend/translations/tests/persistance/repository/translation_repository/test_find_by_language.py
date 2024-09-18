from tests.factory import TranslationFactory, LanguageFactory
from translations.persistance.repository import TranslationRepository


def test_find_by_languages(translation_repository: TranslationRepository) -> None:
    language = LanguageFactory()
    translations = TranslationFactory.create_batch(5, language=language)

    result = translation_repository.find_by_language(language.id)

    assert translations == result
