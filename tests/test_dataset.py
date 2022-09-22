import pytest
import streamdatasetjson as dj


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

    def test_correctly_loads_the_records_property_for_jsons_with_one_dataset(self, fixture):
        (simple_dataset, _) = fixture
        assert simple_dataset.records == 600

    def test_correctly_loads_the_records_property_for_jsons_with_multiple_datsets(self, fixture):
        (_, multi_dataset) = fixture
        assert multi_dataset.records == 200

    def test_correctly_loads_the_label_property_for_jsons_with_one_dataset(self, fixture):
        (simple_dataset, _) = fixture
        assert simple_dataset.label == "Demographics"

    def test_correctly_loads_the_label_property_for_jsons_with_multiple_datsets(self, fixture):
        (_, multi_dataset) = fixture
        assert multi_dataset.label == "Adverse Events"

    def test_correctly_loads_the_items_property_for_jsons_with_one_dataset(self, fixture):
        (simple_dataset, _) = fixture
        assert len(simple_dataset.items) == 5

    def test_correctly_loads_the_items_property_for_jsons_with_multiple_datsets(self, fixture):
        (_, multi_dataset) = fixture
        assert len(multi_dataset.items) == 5

    def test_correctly_loads_the_variables_property_for_jsons_with_one_dataset(self, fixture):
        (simple_dataset, _) = fixture
        assert simple_dataset.variables == ["ITEMGROUPDATASEQ", "STUDYID", "USUBJID", "DOMAIN", "AGE"]

    def test_correctly_loads_the_variables_property_for_jsons_with_multiple_datsets(self, fixture):
        (_, multi_dataset) = fixture
        assert multi_dataset.variables == ["ITEMGROUPDATASEQ", "STUDYID", "USUBJID", "DOMAIN", "AGE"]


class TestDatasetItemsProperty:
    def test_correctly_loads_all_attributes_for_each_of_the_items_property_for_jsons_with_one_dataset(self):
        with dj.DatasetJSON(SIMPLE_DATASET_PATH) as json:
            simple_dataset = json.get_dataset("DM")
            first_item = simple_dataset.items[0]
            assert first_item.oid == "ITEMGROUPDATASEQ" and first_item.name == "ITEMGROUPDATASEQ" \
                and first_item.label == "Record identifier" and first_item.type == "integer"

    def test_correctly_loads_all_attributes_for_each_of_the_items_property_for_jsons_with_multiple_datasets(self):
        with dj.DatasetJSON(MULTIPLE_DATASETS_PATH) as json:
            multi_dataset = json.get_dataset("AE")
            first_item = multi_dataset.items[0]
            assert first_item.oid == "ITEMGROUPDATASEQ" and first_item.name == "ITEMGROUPDATASEQ" \
                and first_item.label == "Record identifier" and first_item.type == "integer"
