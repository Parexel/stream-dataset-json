import os
import guppy

from dataset import Dataset
from datasetjson import DatasetJSON


if __name__ == "__main__":
    FILE_PATH = os.path.abspath("./datasets/adlbc.json")

    with DatasetJSON(FILE_PATH) as dataset_json:
        adlbc: Dataset = dataset_json.get_dataset("ADLBC")

        h = guppy.hpy()
        print(h.heap())

        print()

        size = 0
        for o in adlbc.observations:
            size += 1

        print(size)

        h = guppy.hpy()
        print(h.heap())

