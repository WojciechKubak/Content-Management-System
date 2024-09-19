from translations.core.exceptions import ConfigurationError
from enum import Enum


def env_to_enum(enum_class: type[Enum], env: str | None) -> Enum:
    for choice in enum_class:
        if choice.value.lower() == env.lower():
            return choice

    raise ConfigurationError(f"Invalid value for {enum_class.__name__}: {env}")
