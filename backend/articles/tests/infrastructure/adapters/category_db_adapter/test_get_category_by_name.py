from articles.infrastructure.adapters.adapters import CategoryDbAdapter
from articles.infrastructure.persistance.entity import CategoryEntity
from tests.factory import CategoryEntityFactory


class TestGetCategoryByName:

    def test_when_not_found(
            self,
            category_db_adapter: CategoryDbAdapter
    ) -> None:
        result = category_db_adapter.get_category_by_name('name')
        assert not result

    def test_when_found(self, category_db_adapter: CategoryDbAdapter) -> None:
        category = CategoryEntityFactory()
        result = category_db_adapter.get_category_by_name(category.name)
        assert CategoryEntity.query.filter_by(name=result.name).first()
