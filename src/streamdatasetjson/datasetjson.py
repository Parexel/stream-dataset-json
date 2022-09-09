from typing import List
import ijson
import utils

from dataset import Dataset
from errors import DatasetNotFoundError


class DatasetJSON:
    """
    Dataset JSON instance. 
    """
    def __enter__(self):
        self._file = open(self._path, "r")
        self._dataset_prefixes = self._generate_dataset_prefixes()
        return self

    def __exit__(self, type, value, traceback):
        self._file.close()

    def __init__(self, path):
        self._path = path

    def get_dataset(self, target_name: str) -> Dataset:
        if target_name not in self._dataset_prefixes.keys():
            raise DatasetNotFoundError(target_name)

        return Dataset(self._file, target_name, self._dataset_prefixes[target_name])
    
    @property
    def available_datasets(self) -> List[str]:
        return self._dataset_prefixes.keys()

    def _generate_dataset_prefixes(self):
        events = ijson.parse(self._file)

        prefixes = []
        for prefix, event, value in events:
            if prefix == "clinicalData.itemGroupData" or prefix == "referenceData.itemGroupData":
                if event == "map_key":
                    prefixes.append(f"{prefix}.{value}")

        return { utils.load_prefix(self._file, f"{prefix}.name"): prefix for prefix in prefixes }