import pytest
import streamdatasetjson as dj


ADAE_PATH = "./examples/adae.json"
MULTIPLE_DATASETS_PATH = "./examples/multiple_datasets.json"
NON_EXISTENT_PATH = "./examples/non_existent.json"


class TestDatasetJSONAvailableDatasets:
    def test_correctly_returns_all_available_datasets_when_json_contains_just_one_dataset(self):
        with dj.DatasetJSON(ADAE_PATH) as json:
            assert json.available_datasets == ["ADAE"]

    def test_correctly_returns_all_available_datasets_when_json_contains_multiple_datasets(self):
        with dj.DatasetJSON(MULTIPLE_DATASETS_PATH) as json:
            assert json.available_datasets == ["DM", "AE"]

    # def test_fails_if_the_given_json_path_is_invalid(self):
    #     # TODO
    #     pass


class TestDatasetJSONGetDataset:
    def test_correctly_returns_the_required_dataset_when_json_contains_just_one_dataset(self):
        with dj.DatasetJSON(ADAE_PATH) as json:
            dataset = json.get_dataset("ADAE")
            assert dataset.name == "ADAE"

    def test_correctly_returns_the_required_dataset_when_json_contains_multiple_datasets(self):
        with dj.DatasetJSON(MULTIPLE_DATASETS_PATH) as json:
            dataset = json.get_dataset("AE")
            assert dataset.name == "AE"

    def test_fails_if_the_given_dataset_name_does_not_exist_in_the_given_json(self):
        with dj.DatasetJSON(ADAE_PATH) as json:
            with pytest.raises(dj.DatasetNotFoundError):
                json.get_dataset("NONT_EXISTENT_DATASET")
