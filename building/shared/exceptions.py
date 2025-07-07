class UnauthorizedError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        make_response(self.message, 401)

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        make_response(self.message, 400)

class TokenExpiredError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        make_response(self.message, 401)

class BadRequestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        make_response(self.message, 400)

class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        make_response(self.message, 404)

class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        make_response(self.message, 500)
