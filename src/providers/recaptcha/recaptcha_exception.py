class RecaptchaExpectedException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        

class FaildCreateTaskException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        

class FaildSolutionException(Exception):
    def __init__(self, message: str):
        super().__init__(message)   