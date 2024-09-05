

class UserNameInUseException(Exception):
    def __init__(self, message="Username already in use"):
        self.message = message
        super().__init__(self.message)
    

class EmailInUseException(Exception):
    def __init__(self, message="Email already in use"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyActiveException(Exception):
    def __init__(self, message="User already active"):
        self.message = message
        super().__init__(self.message)


class UserNotActiveException(Exception):
    def __init__(self, message="User not active"):
        self.message = message
        super().__init__(self.message)


class IncorrectPasswordException(Exception):
    def __init__(self, message="Incorrect password"):
        self.message = message
        super().__init__(self.message)


class CommentNotFoundException(Exception):
    def __init__(self, message="Comment not found"):
        self.message = message
        super().__init__(self.message)


class InvalidRoleException(Exception):
    def __init__(self, message="Invalid role"):
        self.message = message
        super().__init__(self.message)


class ActivationLinkExpiredException(Exception):
    def __init__(self, message="Activation link expired"):
        self.message = message
        super().__init__(self.message)


class NotCommentOwnerException(Exception):
    def __init__(self, message="Not the owner of the comment"):
        self.message = message
        super().__init__(self.message)
