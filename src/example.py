import os
import guppy

# from datasetjson import DatasetJSON
# from datasetjson import Dataset
from dataset import Dataset
from datasetjson import DatasetJSON


if __name__ == "__main__":
    FILE_PATH = os.path.abspath("./examples/datasets/adlbc.json")

    with DatasetJSON(FILE_PATH) as dataset_json:
        adlbc = dataset_json.get_dataset("ADLBC")
        # adlbc: Dataset = dataset_json.get_dataset("ADLBC")

        h = guppy.hpy()
        print(h.heap())
