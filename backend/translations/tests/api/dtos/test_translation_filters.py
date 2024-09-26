from translations.api.dtos import TranslationFilters


class TestTranslationFilters:
    query_params: dict[str, str | int | None] = {
        "status": "completed",
        "language_id": 1,
        "article_id": None,
        "translator_id": None,
    }

    def test_from_query_params(self) -> None:
        result = TranslationFilters.from_query_params(self.query_params)
        assert self.query_params.items() == result.__dict__.items()

    def test_to_dict(self) -> None:
        filters = TranslationFilters(**self.query_params)
        result = filters.to_dict()
        assert {k: v for k, v in self.query_params.items() if v is not None} == result
