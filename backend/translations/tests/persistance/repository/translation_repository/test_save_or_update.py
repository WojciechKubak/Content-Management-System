from tests.factory import TranslationFactory
from translations.persistance.repository import TranslationRepository
from translations.persistance.entity import Translation
from translations.persistance.configuration import sa


class TestSaveOrUpdate:

    def test_when_saved(self, translation_repository: TranslationRepository) -> None:
        translation = TranslationFactory()
        translation_repository.save_or_update(translation)
        assert sa.session.query(Translation).filter_by(id=translation.id).first()

    def test_when_updated(self, translation_repository: TranslationRepository) -> None:
        translation = TranslationFactory()
        updated_title = f"new {translation.title}"
        translation.title = updated_title

        translation_repository.save_or_update(translation)

        assert sa.session.query(Translation).filter_by(id=translation.id).first().title == updated_title
    