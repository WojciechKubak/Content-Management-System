from translations.persistance.entity import Translation
from dataclasses import dataclass
from typing import Self


@dataclass
class ChatGptTitleTranslationDTO:
    """
    A data transfer object for title translation requests to the OpenAI GPT-3 model.

    Attributes:
        text (str): The title to be translated.
        language (str): The language to translate the title into.
        role (str): The role of the user. Default is 'user'.
    """

    text: str
    language: str
    role: str = 'user'

    def __str__(self) -> str:
        """
        Returns a string representation of the translation request.
        """
        return f'Translate this title: "{self.text}" to {self.language} language'
    
    @classmethod
    def from_entity(cls, translation: Translation) -> Self:
        """
        Creates a new instance of the class from a Translation entity.

        Args:
            translation (Translation): The Translation entity.

        Returns:
            Self: A new instance of the class.
        """
        return cls(
            text=translation.article.title,
            language=translation.language.name
        )


@dataclass
class ChatGptContentTranslationDTO:
    """
    A data transfer object for content translation requests to the OpenAI GPT-3 model.

    Attributes:
        text (str): The content to be translated.
        language (str): The language to translate the content into.
        role (str): The role of the user. Default is 'user'.
    """

    text: str
    language: str
    role: str = 'user'

    def __str__(self) -> str:
        """
        Returns a string representation of the translation request.
        """
        return f'Translate this content of article: "{self.text}" to {self.language} language, keep all tags as they are'
    
    @classmethod
    def from_entity(cls, translation: Translation, content: str) -> Self:
        """
        Creates a new instance of the class from a Translation entity.

        Args:
            translation (Translation): The Translation entity.

        Returns:
            Self: A new instance of the class.
        """
        return cls(
            text=content,
            language=translation.language.name
        )
