class ResponseError(Exception):
    def __init__(self, message="Error with the server response"):
        self.message = message
        super().__init__(self.message)