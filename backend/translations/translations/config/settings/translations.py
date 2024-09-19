from backend.translations.translations.enums.enums import TranslationType
from config.env import env_to_enum
import os


TRANSLATION_TYPE_STRATEGY: TranslationType = env_to_enum(
    TranslationType, os.getenv("TRANSLATION_TYPE", TranslationType.LOCAL.value)
)

if TRANSLATION_TYPE_STRATEGY == TranslationType.OPENAI:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
