from tests.factory import LanguageFactory
from translations.persistance.repository import LanguageRepository
from translations.persistance.entity import Language
from translations.persistance.configuration import sa


def test_delete_by_id(language_repository: LanguageRepository) -> None:
    language = LanguageFactory()
    language_repository.delete_by_id(language.id)
    assert not sa.session.query(Language).filter_by(id=language.id).first()
