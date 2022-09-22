from io import TextIOWrapper
from typing import Iterable, NamedTuple, NewType, Optional
import streamdatasetjson.utils as utils


Row = NewType("Row", 'list[str]')
JSONFileObject = NewType("JSONFileObject", TextIOWrapper)


class Item(NamedTuple):
    oid:    str
    name:   str
    label:  str
    type:   str
    length: Optional[int]


class Dataset:
    """
    Dataset. Should not be instantiated directly.
    """

    def __init__(self, dataset_json_file: JSONFileObject, name: str, prefix: str):
        self._df = dataset_json_file
        self._prefix = prefix
        self._name = name
        self._records = self._get_attribute("records")
        self._label = self._get_attribute("label")
        self._items = [self._raw_to_item(raw_item)
                       for raw_item in self._get_attribute("items")]

    def _get_attribute(self, attr_name: str):
        return utils.load_prefix(self._df, f"{self._prefix}.{attr_name}")

    def _raw_to_item(self, raw_item: dict) -> Item:
        return Item(oid=raw_item["OID"],
                    name=raw_item["name"],
                    label=raw_item["label"],
                    type=raw_item["type"],
                    length=raw_item.get("length", None))

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
    def items(self) -> 'list[Item]':
        return self._items

    @property
    def variables(self) -> 'list[str]':
        return [meta["name"] for meta in self.items]
