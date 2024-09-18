from tests.factory import TranslationFactory, LanguageFactory
from translations.api.exceptions import EntityNotFoundError
from translations.api.service import ApiService
import pytest


class TestGetTranslationByLanguage:

    def test_when_language_not_found(self, api_service: ApiService) -> None:
        with pytest.raises(EntityNotFoundError) as e:
            api_service.get_translations_by_language(999)
        assert "Language not found" == str(e.value)

    def test_when_found(self, api_service: ApiService) -> None:
        language = LanguageFactory()
        translations = TranslationFactory.create_batch(5, language=language)

        result = api_service.get_translations_by_language(language.id)

        assert len(translations) == len(result)
