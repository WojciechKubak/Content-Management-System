

class UserNameInUseException(Exception):
    def __init__(self, message="Username already in use"):
        super().__init__(message)
    

class EmailInUseException(Exception):
    def __init__(self, message="Email already in use"):
        super().__init__(message)


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        super().__init__(message)


class UserAlreadyActiveException(Exception):
    def __init__(self, message="User already active"):
        super().__init__(message)


class UserNotActiveException(Exception):
    def __init__(self, message="User not active"):
        super().__init__(message)


class IncorrectPasswordException(Exception):
    def __init__(self, message="Incorrect password"):
        super().__init__(message)


class CommentNotFoundException(Exception):
    def __init__(self, message="Comment not found"):
        super().__init__(message)
