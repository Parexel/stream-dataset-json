
class Dataset:
    def __init__(self, name, raw_dict):
        self._name = name
        self._raw_dict = raw_dict
    
    @property
    def name(self):
        return self._name

    @property
    def items(self):
        return self._raw_dict["items"]