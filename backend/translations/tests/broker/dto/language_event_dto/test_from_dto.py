from translations.broker.dto import LanguageEventDTO, LanguageEventType


def test_from_dto() -> None:
    dto = {"id": 1, "name": "English", "code": "en", "event_type": "CREATE"}
    result = LanguageEventDTO.from_dto(dto)

    assert dto["id"] == result.id_
    assert LanguageEventType[dto["event_type"]] == result.event_type
