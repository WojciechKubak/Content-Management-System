from translations.core.exceptions import ConfigurationError
from pathlib import Path
from enum import Enum


PROJECT_ROOT: str = Path(__file__).resolve().parent.parent


def env_to_bool(env: str | None) -> bool:
    return str(env).upper() in ["TRUE", "1", "YES"]


def env_to_enum(enum_class: type[Enum], env: str | None) -> Enum:
    for choice in enum_class:
        if choice.value.lower() == env.lower():
            return choice

    raise ConfigurationError(f"Invalid value for {enum_class.__name__}: {env}")
