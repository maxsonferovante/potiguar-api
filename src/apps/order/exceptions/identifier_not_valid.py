

class IdentifierNotValid(Exception):
    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Identifier '{identifier}' is not valid.")