from tests.factories import TranslationFactory, LanguageFactory, Translation, sa
from translations.db.repositories import TranslationRepository


def test_find_by_language(translation_repository: TranslationRepository) -> None:
    language = LanguageFactory()
    TranslationFactory.create_batch(size=5, language=language)

    result = translation_repository.find_by_language(language.id)

    assert (
        sa.session.query(Translation).filter_by(language_id=language.id).all() == result
    )
