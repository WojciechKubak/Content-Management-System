

class ChatGptServiceError(Exception):

    def __init__(self, message="Chat GPT service error"):
        self.message = message
        super().__init__(self.message)
