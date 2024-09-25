from translations.common.models import SimpleModel
from translations.db.repositories import CrudRepositoryORM
from translations.db.configuration import sa
from tests.factories import SimpleModelFactory
from dataclasses import dataclass


@dataclass
class SimpleModelRepository(CrudRepositoryORM[SimpleModel]):
    pass


class TestCrudRepository:
    simple_repository = SimpleModelRepository(sa)

    def test_save_or_update(self) -> None:
        model = SimpleModelFactory()
        self.simple_repository.save_or_update(model)

        assert model == sa.session.query(SimpleModel).first()

        model.name = f"new_{model.name}"
        self.simple_repository.save_or_update(model)

        assert model == sa.session.query(SimpleModel).first()

    def test_find_by_id(self) -> None:
        model = SimpleModelFactory()
        result = self.simple_repository.find_by_id(model.id)

        assert model == result

        result = self.simple_repository.find_by_id(999)

        assert result is None

    def test_find_all(self) -> None:
        models = SimpleModelFactory.create_batch(5)
        result = self.simple_repository.find_all(limit=10, offset=0)
        assert models == result

    def test_delete_by_id(self) -> None:
        model = SimpleModelFactory()
        self.simple_repository.delete_by_id(model.id)
        assert 0 == sa.session.query(SimpleModel).count()
