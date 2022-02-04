import json
from abc import ABC
from os import remove
from typing import Any, Iterator
from urllib.request import urlretrieve
from zipfile import ZipFile

from cattr import structure

from foodprep.const import EDITION, TEMP_PATH
from foodprep.dataset_models import IngredientModel
from foodprep.fdc_models import FDCFoodItemModel
from foodprep.utils import count_lines, measure

__all__ = [
    "Dataset",
    "BrandedDataset",
    "FoundationDataset",
    "LegacyDataset",
    "SurveyDataset",
]


class Dataset(ABC):
    name: str

    @classmethod
    @property
    def temp_zip_path(cls):
        return TEMP_PATH / f"{cls.name}.zip"

    @classmethod
    @property
    def temp_ndjson_path(cls):
        return TEMP_PATH / f"{cls.name}.ndjson"

    def temp_zip_download(self, force: bool = False):
        if self.temp_zip_path.exists() and not force:
            return
        with measure(f"downloading {self.name}"):
            src_zip_filename = f"FoodData_Central_{self.name}_food_json_{EDITION}.zip"
            url = f"https://fdc.nal.usda.gov/fdc-datasets/{src_zip_filename}"
            urlretrieve(url, self.temp_zip_path)

    def temp_zip_extract(self, force: bool = False):
        if self.temp_ndjson_path.exists() and not force:
            return
        src_json_filename = f"FoodData_Central_{self.name}_food_json_{EDITION}.json"
        src_json_path = TEMP_PATH / src_json_filename
        with measure(f"extracting {self.name}"):
            with ZipFile(self.temp_zip_path, "r") as zipfile:
                zipfile.extract(src_json_filename, TEMP_PATH)
            with (
                open(src_json_path, "r") as src_json_file,
                open(self.temp_ndjson_path, "w") as temp_ndjson_file,
            ):
                line_count = count_lines(src_json_path)
                eof = line_count - 1
                for line_idx, line in enumerate(src_json_file):
                    if 1 <= line_idx < eof:
                        temp_ndjson_file.write(line.rstrip("\n").rstrip(",") + "\n")
                remove(src_json_path)

    def __iter__(self) -> Iterator[IngredientModel]:
        with (
            measure(f"parsing {self.name}"),
            open(self.temp_ndjson_path, "r") as lines,
        ):
            for line in lines:
                source_data: dict[str, Any] = json.loads(line)
                fdc_model = structure(source_data, FDCFoodItemModel)
                yield IngredientModel.from_fdc_data(fdc_model)


class BrandedDataset(Dataset):
    name = "branded"


class LegacyDataset(Dataset):
    name = "sr_legacy"


class FoundationDataset(Dataset):
    name = "foundation"


class SurveyDataset(Dataset):
    name = "survey"
