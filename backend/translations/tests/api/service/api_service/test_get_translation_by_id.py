from tests.factory import TranslationFactory
from translations.api.exceptions import EntityNotFoundError
from translations.api.service import ApiService
import pytest


class TestGetTranslationById:

    def test_when_no_translation(self, api_service: ApiService) -> None:
        with pytest.raises(EntityNotFoundError) as e:
            api_service.get_translation_by_id(999)
        assert 'Translation not found' == str(e.value)        

    def test_when_found(self, api_service: ApiService) -> None:
        translation = TranslationFactory()
        result = api_service.get_translation_by_id(translation.id)
        assert translation.id == result.id_
