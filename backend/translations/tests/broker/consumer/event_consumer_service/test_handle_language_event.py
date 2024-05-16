from tests.factory import LanguageFactory, LanguageEventDTOFactory
from translations.broker.consumer import EventConsumerService
from translations.api.exceptions import (
    EntityNotFoundError, 
    InvalidStatusOperationError, 
    EntityAlreadyExistsError
)
from translations.broker.dto import LanguageEventType
import pytest


class TestHandleLanguageEvent:

    def test_when_exists_on_create(self, event_consumer_service: EventConsumerService) -> None:
        language = LanguageFactory()
        dto = LanguageEventDTOFactory(id_=language.id, event_type=LanguageEventType.CREATE)

        with pytest.raises(EntityAlreadyExistsError) as e:
            event_consumer_service.handle_language_event(dto)

        assert EntityAlreadyExistsError('Language already exists').message == str(e.value)

    def test_when_not_found_on_update(self, event_consumer_service: EventConsumerService) -> None:
        dto = LanguageEventDTOFactory(event_type=LanguageEventType.UPDATE)

        with pytest.raises(EntityNotFoundError) as e:
            event_consumer_service.handle_language_event(dto)
        
        assert EntityNotFoundError('Language not found').message == str(e.value)

    def test_when_not_found_on_delete(self, event_consumer_service: EventConsumerService) -> None:
        dto = LanguageEventDTOFactory(event_type=LanguageEventType.DELETE)

        with pytest.raises(EntityNotFoundError) as e:
            event_consumer_service.handle_language_event(dto)

        assert EntityNotFoundError('Language not found').message == str(e.value)

    def test_when_unsupported_event_type(self, event_consumer_service: EventConsumerService) -> None:
        dto = LanguageEventDTOFactory(event_type='UNSUPPORTED')

        with pytest.raises(InvalidStatusOperationError) as e:
            event_consumer_service.handle_language_event(dto)
        
        assert InvalidStatusOperationError().message == str(e.value)
