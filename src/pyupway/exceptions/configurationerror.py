class ConfigurationError(Exception):
    def __init__(self, message="Error in configuration"):
        self.message = message
        super().__init__(self.message)
