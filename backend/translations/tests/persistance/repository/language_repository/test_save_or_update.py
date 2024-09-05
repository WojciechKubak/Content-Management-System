from tests.factory import LanguageFactory
from translations.persistance.repository import LanguageRepository
from translations.persistance.entity import Language
from translations.persistance.configuration import sa


class TestSaveOrUpdate:

    def test_when_saved(self, language_repository: LanguageRepository) -> None:
        language = LanguageFactory()
        result = language_repository.save_or_update(language)
        assert sa.session.query(Language).filter_by(id=result.id).first()

    def test_when_updated(self, language_repository: LanguageRepository) -> None:
        language = LanguageFactory()
        updated_code = f"N{language.code}"
        language.code = updated_code

        language_repository.save_or_update(language)

        assert sa.session.query(Language).filter_by(id=language.id).first().code == updated_code
