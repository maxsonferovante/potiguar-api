class ConflictProcessOrderException(Exception):
    def __init__(self, 
                 license_plate: str,
                 renavam: str,
                 identifier: str,
                 task_id: str,):
        
        self.license_plate = license_plate
        self.renavam = renavam
        self.identifier = identifier
        self.task_id = task_id
        super().__init__(
            "Conflict process order: license_plate: {}, renavam: {}, identifier: {}, task_id: {}".format(
                license_plate, renavam, identifier, task_id
            )
        )