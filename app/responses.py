class Response:
    def __init__(self, message):
        self.message = message


class SttResponse(Response):
    def __init__(self, message, time=None):
        super().__init__(message)
        self.time = time


class HotWordResponse(Response):
    def __init__(self, message):
        super().__init__(message)
