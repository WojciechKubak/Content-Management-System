from translations.services.translations import (
    LANGUAGE_NOT_FOUND_ERROR_MSG,
    TRANSLATION_ALREADY_EXISTS_ERROR_MSG,
    ValidationError,
    TranslationRequest,
    handle_translation_request,
)
from unittest.mock import MagicMock
import pytest


@pytest.fixture(scope="session")
def mock_request() -> MagicMock:
    mock_request = MagicMock(spec=TranslationRequest)
    mock_request.id_ = 1
    mock_request.language_id = 1

    return mock_request


def test_handle_translation_request_raises_validation_error_on_missing_language(
    mock_language_repository, mock_request
) -> None:
    mock_language_repository.find_by_id.return_value = None

    with pytest.raises(ValidationError, match=LANGUAGE_NOT_FOUND_ERROR_MSG):
        handle_translation_request(translation_request=mock_request)

    mock_language_repository.find_by_id.assert_called_once_with(
        mock_request.language_id
    )


def test_handle_translation_request_raises_validation_error_on_already_existing_translation(
    mock_language_repository, mock_translation_repository, mock_request
) -> None:
    mock_language_repository.find_by_id.return_value = MagicMock()
    mock_translation_repository.find_by_language_and_article.return_value = MagicMock()

    with pytest.raises(ValidationError, match=TRANSLATION_ALREADY_EXISTS_ERROR_MSG):
        handle_translation_request(translation_request=mock_request)

    mock_language_repository.find_by_id.assert_called_once_with(
        mock_request.language_id
    )
    mock_translation_repository.find_by_language_and_article.assert_called_once_with(
        mock_request.language_id, mock_request.id_
    )


def test_handle_translation_on_success_creates_article_and_translations_db_records(
    mock_language_repository,
    mock_translation_repository,
    mock_article_repository,
    mock_request,
) -> None:
    mock_language_repository.find_by_id.return_value = MagicMock()
    mock_translation_repository.find_by_language_and_article.return_value = None
    mock_article_repository.find_by_id.return_value = None

    mock_article_entity = MagicMock()
    mock_translation_entity = MagicMock()
    mock_request.to_article_entity.return_value = mock_article_entity
    mock_request.to_translation_entity.return_value = mock_translation_entity

    handle_translation_request(translation_request=mock_request)

    mock_article_repository.find_by_id.assert_called_once_with(mock_request.id_)
    mock_article_repository.save_or_update.assert_called_once_with(mock_article_entity)
    mock_translation_repository.save_or_update.assert_called_once_with(
        mock_translation_entity
    )


def test_handle_translation_on_success_skips_article_and_creates_translation_db_record(
    mock_language_repository,
    mock_translation_repository,
    mock_article_repository,
    mock_request,
) -> None:
    mock_language_repository.find_by_id.return_value = MagicMock()
    mock_translation_repository.find_by_language_and_article.return_value = None
    mock_article_repository.find_by_id.return_value = MagicMock()

    mock_article_entity = MagicMock()
    mock_translation_entity = MagicMock()
    mock_request.to_article_entity.return_value = mock_article_entity
    mock_request.to_translation_entity.return_value = mock_translation_entity

    handle_translation_request(translation_request=mock_request)

    mock_article_repository.find_by_id.assert_called_once_with(mock_request.id_)
    mock_article_repository.save_or_update.assert_not_called()
    mock_translation_repository.save_or_update.assert_called_once_with(
        mock_translation_entity
    )
