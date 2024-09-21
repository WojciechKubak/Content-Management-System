from tests.factories import TranslationFactory, Translation, sa
from translations.db.repositories import TranslationRepository


def test_find_by_language_and_article(
    translation_repository: TranslationRepository,
) -> None:
    model = TranslationFactory()

    result = translation_repository.find_by_language_and_article(
        model.language.id, model.article.id
    )
    expected = (
        sa.session.query(Translation)
        .filter_by(language_id=model.language.id)
        .filter_by(article_id=model.article.id)
        .first()
    )

    assert expected == result
