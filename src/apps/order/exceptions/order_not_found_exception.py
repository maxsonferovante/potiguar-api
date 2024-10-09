class OrderNotFoundException(Exception):
    def __init__(self, identifier: str):
        super().__init__("Order {} not found".format(identifier))
        self.identifier = identifier