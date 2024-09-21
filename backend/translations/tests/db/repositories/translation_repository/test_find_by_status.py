from tests.factories import TranslationFactory, Translation, sa
from translations.db.repositories import TranslationRepository


def test_find_by_status(translation_repository: TranslationRepository) -> None:
    status = Translation.StatusType.COMPLETED
    TranslationFactory.create_batch(size=5, status=status)

    result = translation_repository.find_by_status(status)

    assert sa.session.query(Translation).filter_by(status=status).all() == result
