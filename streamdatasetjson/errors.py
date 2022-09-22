
class DatasetNotFoundError(Exception):
    def __init__(self, name):
        super().__init__(f"Dataset {name} was not found.")
