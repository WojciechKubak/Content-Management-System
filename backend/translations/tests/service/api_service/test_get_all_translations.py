from tests.factory import TranslationFactory
from translations.api.service import ApiService


def test_get_all_translations(api_service: ApiService) -> None:
    translations = TranslationFactory.create_batch(5)
    result = api_service.get_all_translations()
    assert len(translations) == len(result)
