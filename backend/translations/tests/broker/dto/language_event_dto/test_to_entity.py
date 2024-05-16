from tests.factory import LanguageEventDTOFactory


def test_to_entity() -> None:
    dto = LanguageEventDTOFactory()
    
    result = dto.to_entity()
    
    assert dto.id_ == result.id
    assert dto.name == result.name
    assert dto.code == result.code
