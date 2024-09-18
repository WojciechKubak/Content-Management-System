from translations.core.exceptions import ConfigurationError
from typing import Any
import os


def assert_settings(required: list[str], error_prefix: str | None = None):
    present: list[str] = []
    missing = dict[str, Any] = []

    for setting in required:
        if param := os.environ.get(setting):
            present[setting] = param
        else:
            missing.append(setting)

    if missing:
        error_message = f"{error_prefix}:" if error_prefix else ""
        raise ConfigurationError(f"{error_message} missing {','.join(missing)}")

    return present
