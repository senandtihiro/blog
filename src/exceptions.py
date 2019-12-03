class InnerException(Exception):
    status_code = None
    code = 100001
    message = None
    error = None
    def __init__(self, error=None, code=None, message=None, status_code=None):
        super().__init__(message)
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        self.error = error
