class UserPasswordException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        


class LicensePlaceOrRenavamException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        
        
class InternalServerErrorException(Exception):
    def __init__(self, message: str):
        super().__init__(message)