from io import TextIOWrapper
from typing import Iterable, NewType
import utils


Row = NewType("Row", 'list[str]')
VarMeta = NewType("VarMeta", dict)

JSONFileObject = NewType("JSONFileObject", TextIOWrapper)

class Dataset:
    """
    Dataset. Should not be instantiated manually.
    """
    def __init__(self, dataset_json_file: JSONFileObject, name: str, prefix: str):
        self._df = dataset_json_file
        self._prefix = prefix
        self._name = name
        self._records = self._get_attribute("records")
        self._label   = self._get_attribute("label")
        self._items   = self._get_attribute("items")

    def _get_attribute(self, attr_name: str):
        return utils.load_prefix(self._df, f"{self._prefix}.{attr_name}")
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def observations(self) -> Iterable[Row]:
        return utils.reread_prefix(self._df, f"{self._prefix}.itemData.item")

    @property
    def records(self) -> int:
        return self._records

    @property
    def label(self) -> str:
        return self._label

    @property
    def items(self) -> VarMeta:
        return self._items

    @property
    def variables(self) -> 'list[str]':
        return [ meta["name"] for meta in self.items ]