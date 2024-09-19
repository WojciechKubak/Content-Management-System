class ConfigurationError(Exception):
    def __init__(self, message: str):
        self.message = message


class ApplicationError(Exception):
    def __init__(self, message: str):
        self.message = message


class StorageError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class TranslationError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)
