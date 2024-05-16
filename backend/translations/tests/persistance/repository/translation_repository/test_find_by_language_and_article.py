from tests.factory import TranslationFactory
from translations.persistance.repository import TranslationRepository
from translations.persistance.configuration import sa


def test_find_by_language_and_article(translation_repository: TranslationRepository) -> None:
    translation = TranslationFactory()
    sa.session.commit()

    result = translation_repository.find_by_language_and_article(
        translation.language_id, translation.article_id
    )
    
    assert translation == result
