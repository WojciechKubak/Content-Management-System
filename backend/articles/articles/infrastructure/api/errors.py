class ApplicationError(Exception):
    def __init__(self, message: str = "Application error"):
        self.message = message
        super().__init__(self.message)
