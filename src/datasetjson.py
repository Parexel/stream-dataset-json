import ijson
from dataset import Dataset
from errors import DatasetNotFoundError


class DatasetJSON:
    def __enter__(self):
        self._file = open(self._path, "r")
        return self

    def __exit__(self, type, value, traceback):
        self._file.close()

    def __init__(self, path):
        self._path = path

    def get_dataset(self, target_name):
        datasets = ijson.kvitems(self._file, "clinicalData.itemGroupData")
        for name, data in datasets:
            if name == target_name:
                return data
        
        raise DatasetNotFoundError()