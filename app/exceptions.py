class AppError(Exception):
    status_code = 500

    def __init__(self, message=None, payload=None):
        super().__init__(message or self.__class__.__name__)
        self.message = message or ""
        self.payload = payload or {}

    def to_dict(self):
        body = {"error": self.__class__.__name__, "message": self.message}
        if self.payload:
            body["details"] = self.payload
        return body


class ValidationError(AppError):
    status_code = 400
    def __init__(self, message="Bad Request", payload=None):
        super().__init__(message, payload)


class NotFoundError(AppError):
    status_code = 404
    def __init__(self, message="Not Found", payload=None):
        super().__init__(message, payload)


class ServiceError(AppError):
    status_code = 500
    def __init__(self, message="Internal Server Error", payload=None):
        super().__init__(message, payload)