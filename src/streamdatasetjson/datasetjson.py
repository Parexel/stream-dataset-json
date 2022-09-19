import ijson

from types import TracebackType
from typing import Optional, Type

from streamdatasetjson.dataset import Dataset
from streamdatasetjson.errors import DatasetNotFoundError


class DatasetJSON:
    """
    Dataset JSON instance.
    """

    def __enter__(self):
        return self

    def __exit__(self,
                 type: Optional[Type[BaseException]],
                 value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        self.close()

    def __init__(self, path: str):
        self._path = path
        self._file = open(self._path, "r")
        self._dataset_prefixes = self._generate_dataset_prefixes()

    def get_dataset(self, target_name: str) -> Dataset:
        if target_name not in self._dataset_prefixes.keys():
            raise DatasetNotFoundError(target_name)

        return Dataset(self._file, target_name, self._dataset_prefixes[target_name])

    @property
    def available_datasets(self) -> 'list[str]':
        return list(self._dataset_prefixes.keys())

    def close(self):
        self._file.close()

    def _generate_dataset_prefixes(self) -> dict:
        events = ijson.parse(self._file)

        prefixes = []
        names = []
        last_prefix = None
        for prefix, event, value in events:
            if prefix == "clinicalData.itemGroupData" or prefix == "referenceData.itemGroupData":
                if event == "map_key":
                    last_prefix = f"{prefix}.{value}"
                    prefixes.append(last_prefix)

            if last_prefix and prefix == f"{last_prefix}.name":
                names.append(value)
                last_prefix = None

        return dict(zip(names, prefixes))
