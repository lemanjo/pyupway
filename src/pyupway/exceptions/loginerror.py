class LoginErr(Exception):
    def __init__(self, message="Cannot login"):
        self.message = message
        super().__init__(self.message)

class NotLoggedIn(Exception):
    def __init__(self, message="Not logged in"):
        self.message = message
        super().__init__(self.message)