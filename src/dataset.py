import ijson


class Dataset:
    def __init__(self, dataset_json_file, name):
        self._df = dataset_json_file
        self._name = name
        self._dataset_prefix = f"clinicalData.itemGroupData.{self.name}"

        self._records = self._get_attribute("records")
        self._label   = self._get_attribute("label")
        self._items   = self._get_attribute("items")

    def _read_prefix(self, prefix):
        self._df.seek(0)
        return ijson.items(self._df, f"{self._dataset_prefix}.{prefix}")


    def _get_attribute(self, attr_name):
        return next(self._read_prefix(attr_name))
    
    @property
    def name(self):
        return self._name

    @property
    def observations(self):
        return self._read_prefix("itemData.item")

    @property
    def records(self):
        return self._records

    @property
    def label(self):
        return self._label

    @property
    def items(self):
        return self._items