

class EntityNotFoundError(Exception):

    def __init__(self, message='Entity not found') -> None:
        self.message = message
        super().__init__(self.message)


class EntityAlreadyExistsError(Exception):

    def __init__(self, message='Entity already exists') -> None:
        self.message = message
        super().__init__(self.message)


class TranslationNotPendingError(Exception):

    def __init__(self, message: str = 'Translation is not pending'):
        self.message = message
        super().__init__(self.message)


class MissingDataError(Exception):

    def __init__(self, message='No data provided') -> None:
        self.message = message
        super().__init__(self.message)


class InvalidRedactorIdError(Exception):
    
    def __init__(self, message="Invalid redactor id"):
        self.message = message
        super().__init__(self.message)


class TranslationAlreadyReleasedError(Exception):
    
    def __init__(self, message="Translation already released"):
        self.message = message
        super().__init__(self.message)


class InvalidStatusOperationError(Exception):

    def __init__(self, message="Invalid status operation"):
        self.message = message
        super().__init__(self.message)
