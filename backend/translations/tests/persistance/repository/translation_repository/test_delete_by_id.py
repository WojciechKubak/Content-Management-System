from tests.factory import TranslationFactory
from translations.persistance.repository import TranslationRepository
from translations.persistance.entity import Translation
from translations.persistance.configuration import sa


def test_delete_by_id(translation_repository: TranslationRepository) -> None:
    translation = TranslationFactory()
    translation_repository.delete_by_id(translation.id)
    assert not sa.session.query(Translation).filter_by(id=translation.id).first()
