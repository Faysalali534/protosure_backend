class ExternalServiceError(Exception):

    def __init__(self, error_code=400, message="Github reported issue , please retry or contact admin"):
        self.message = message
        self.error_code = error_code

        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class concurrencyError(Exception):

    def __init__(self, error_code=409, message="Concurrency issue was captured on update , try transaction again"):
        self.message = message
        self.error_code = error_code

        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
