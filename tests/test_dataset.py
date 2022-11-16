import collections
import pytest
import streamdatasetjson as dj
import psutil
import os
import json


BIG_DATASET_PATH = "./examples/adlbc.json"
ADAE_DATASET_PATH = "./examples/adae.json"
SIMPLE_DATASET_PATH = "./examples/simple_dataset.json"
MULTIPLE_DATASETS_PATH = "./examples/multiple_datasets.json"
NON_EXISTENT_PATH = "./examples/non_existent.json"


class TestDatasetLoadedProperties:
    @pytest.fixture(scope="session", autouse=True)
    def fixture(self):
        simple_json = dj.DatasetJSON(SIMPLE_DATASET_PATH)
        multi_json = dj.DatasetJSON(MULTIPLE_DATASETS_PATH)
        simple_dataset = simple_json.get_dataset("DM")
        multi_dataset = multi_json.get_dataset("AE")
        yield simple_dataset, multi_dataset
        simple_json.close()
        multi_json.close()

    def test_correctly_loads_the_records_property_for_jsons_with_one_dataset(
        self, fixture
    ):
        (simple_dataset, _) = fixture
        assert simple_dataset.records == 600

    def test_correctly_loads_the_records_property_for_jsons_with_multiple_datsets(
        self, fixture
    ):
        (_, multi_dataset) = fixture
        assert multi_dataset.records == 200

    def test_correctly_loads_the_label_property_for_jsons_with_one_dataset(
        self, fixture
    ):
        (simple_dataset, _) = fixture
        assert simple_dataset.label == "Demographics"

    def test_correctly_loads_the_label_property_for_jsons_with_multiple_datsets(
        self, fixture
    ):
        (_, multi_dataset) = fixture
        assert multi_dataset.label == "Adverse Events"

    def test_correctly_loads_the_items_property_for_jsons_with_one_dataset(
        self, fixture
    ):
        (simple_dataset, _) = fixture
        assert len(simple_dataset.items) == 5

    def test_correctly_loads_the_items_property_for_jsons_with_multiple_datsets(
        self, fixture
    ):
        (_, multi_dataset) = fixture
        assert len(multi_dataset.items) == 5

    def test_correctly_loads_the_variables_property_for_jsons_with_one_dataset(
        self, fixture
    ):
        (simple_dataset, _) = fixture
        assert simple_dataset.variables == [
            "ITEMGROUPDATASEQ",
            "STUDYID",
            "USUBJID",
            "DOMAIN",
            "AGE",
        ]

    def test_correctly_loads_the_variables_property_for_jsons_with_multiple_datsets(
        self, fixture
    ):
        (_, multi_dataset) = fixture
        assert multi_dataset.variables == [
            "ITEMGROUPDATASEQ",
            "STUDYID",
            "USUBJID",
            "DOMAIN",
            "AGE",
        ]


class TestDatasetItemsProperty:
    def test_correctly_loads_all_attributes_for_each_of_the_items_property_for_jsons_with_one_dataset(
        self,
    ):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            item = simple_dataset.items[0]
            assert (
                item.oid == "ITEMGROUPDATASEQ"
                and item.name == "ITEMGROUPDATASEQ"
                and item.label == "Record identifier"
                and item.type == "integer"
                and item.length is None
            )

    def test_correctly_loads_all_attributes_for_each_of_the_items_property_for_jsons_with_multiple_datasets(
        self,
    ):
        with dj.DatasetJSON(MULTIPLE_DATASETS_PATH) as json:
            multi_dataset = json.get_dataset("AE")
            item = multi_dataset.items[3]
            assert (
                item.oid == "IT.DOMAIN"
                and item.name == "DOMAIN"
                and item.label == "Domain Identifier"
                and item.type == "string"
                and item.length == 2
            )


class TestDatasetGetUniques:
    def test_correctly_finds_unique_values_for_a_particular_variable_within_all_observations(
        self,
    ):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            uniques = simple_dataset.get_unique_values(variables=["STUDYID"])
            assert uniques.get("STUDYID", None) == set(["MyStudy"])

    def test_correctly_finds_unique_values_for_all_variables_within_all_observations(
        self,
    ):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            uniques = simple_dataset.get_unique_values(variables=["STUDYID", "AGE"])
            assert uniques.get("STUDYID", None) == set(["MyStudy"]) and uniques.get(
                "AGE", None
            ) == set([56, 26])

    def test_correctly_finds_unique_values_for_a_particular_variable_within_the_first_n_observations(
        self,
    ):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            uniques = simple_dataset.get_unique_values(
                variables=["USUBJID"], rows_to_scan=1
            )
            assert uniques.get("USUBJID", None) == set(["001"])

    def test_correctly_finds_unique_values_for_all_variables_within_the_first_n_observations(
        self,
    ):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            uniques = simple_dataset.get_unique_values(
                variables=["STUDYID", "AGE"], rows_to_scan=1
            )
            assert uniques.get("STUDYID", None) == set(["MyStudy"]) and uniques.get(
                "AGE", None
            ) == set([56])

    def test_finds_unique_values_only_for_the_specified_variables(
        self,
    ):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            uniques = simple_dataset.get_unique_values(variables=["DOMAIN", "AGE"])
            assert len(uniques.keys()) == 2

    def test_does_not_fail_if_given_an_invalid_varible_name_returns_an_empty_set(self):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            uniques = simple_dataset.get_unique_values(variables=["INVALID", "AGE"])
            assert len(uniques.keys()) == 2 and len(uniques["INVALID"]) == 0


class TestDatasetObservationsProperty:
    CONSIDERABLE_MEMORY_ENCREASE = 0.15

    def test_looping_over_every_observation_does_not_considerably_encrease_memory_usage(
        self,
    ):
        with dj.DatasetJSON(BIG_DATASET_PATH) as json:
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss
            dataset = json.get_dataset("ADLBC")
            collections.deque(dataset.observations)
            memory_after = process.memory_info().rss
            assert memory_after <= memory_before * (
                1 + self.CONSIDERABLE_MEMORY_ENCREASE
            )

    def test_using_standard_json_library_does_encrease_memory_usage_when_iterating_over_every_observation(
        self,
    ):
        with open(BIG_DATASET_PATH, "rt") as file:
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss
            dataset = json.load(file)["clinicalData"]["itemGroupData"]["ADLBC"]
            collections.deque(dataset["itemData"])
            memory_after = process.memory_info().rss
            assert memory_after > memory_before * (
                1 + self.CONSIDERABLE_MEMORY_ENCREASE
            )
