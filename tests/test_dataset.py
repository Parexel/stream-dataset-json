import pytest
import streamdatasetjson as dj


ADAE_PATH = "./examples/simple_dataset.json"
MULTIPLE_DATASETS_PATH = "./examples/multiple_datasets.json"
NON_EXISTENT_PATH = "./examples/non_existent.json"


class TestDatasetLoadedProperties:
    simple_dataset = None
    multi_dataset = None

    @pytest.fixture(scope="session", autouse=True)
    def fixture(self):
        simple_json = dj.DatasetJSON(ADAE_PATH)
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
