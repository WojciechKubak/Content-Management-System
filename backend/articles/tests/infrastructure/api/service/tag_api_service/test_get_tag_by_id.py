from articles.infrastructure.api.service import TagApiService
from articles.infrastructure.db.entity import TagEntity
from sqlalchemy.orm import Session
import pytest


class TestGetTagById:

    def test_when_not_found(self, tag_api_service: TagApiService) -> None:
        with pytest.raises(ValueError) as err:
            tag_api_service.get_tag_by_id(9999)
        assert 'Tag does not exist' == str(err.value)

    def test_when_found(self, tag_api_service: TagApiService, db_session: Session) -> None:
        db_session.add(TagEntity(id=1, name='name'))
        db_session.commit()
        result = tag_api_service.get_tag_by_id(1)
        assert db_session.query(TagEntity).filter_by(id=result.id_).first()
