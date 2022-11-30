from enum import unique
from io import TextIOWrapper
from typing import Iterable, NamedTuple, NewType, Optional
import streamdatasetjson.utils as utils
import ijson


Row = NewType("Row", "list[str]")
JSONFileObject = NewType("JSONFileObject", TextIOWrapper)


class Item(NamedTuple):
    oid: str
    name: str
    label: str
    type: str
    length: Optional[int]


class Dataset:
    """
    Dataset. Should not be instantiated directly.
    """

    def __init__(self, dataset_json_file: JSONFileObject, name: str, prefix: str):
        self._df = dataset_json_file
        self._prefix = prefix

        self._name = name
        self._records = None
        self._label = None
        self._items = []

        self._df.seek(0)
        item, item_key = None, None
        for prefix, event, value in ijson.parse(self._df):
            if not prefix.startswith(self._prefix):
                continue

            sub_prefix = prefix.replace(self._prefix, "")

            if sub_prefix == ".records":
                self._records = value
            elif sub_prefix == ".label":
                self._label = value
            elif sub_prefix == ".items.item":
                if event == "start_map":
                    item = {}
                elif event == "end_map":
                    self._items.append(self._raw_to_item(item))
                elif event == "map_key":
                    item_key = value
            elif item_key and sub_prefix == f".items.item.{item_key}":
                item[item_key] = value
                item_key = None

    def _raw_to_item(self, raw_item: dict) -> Item:
        return Item(
            oid=raw_item["OID"],
            name=raw_item["name"],
            label=raw_item["label"],
            type=raw_item["type"],
            length=raw_item.get("length", None),
        )

    def get_unique_values(
        self, variables: "list[str]", rows_to_scan: int = 0
    ) -> "dict[str, set]":
        uniques = {name: set() for name in variables}

        scanned_rows = 0
        for row in self.observations:
            if rows_to_scan != 0 and scanned_rows >= rows_to_scan:
                break

            target_item_values = [
                (item.name, value)
                for item, value in zip(self.items, row)
                if item.name in variables
            ]
            for variable, value in target_item_values:
                uniques[variable].add(value)

            scanned_rows = scanned_rows + 1

        return uniques

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
    def items(self) -> "list[Item]":
        return self._items

    @property
    def variables(self) -> "list[str]":
        return [meta.name for meta in self.items]
