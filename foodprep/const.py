from pathlib import Path

import yaml

__all__ = ["DATASET_SOURCES", "OUT_PATH", "TEMP_PATH"]

with open("config.yml", "r") as config_file:
    config_data = yaml.safe_load(config_file)

DATASET_SOURCES: dict[str, str] = config_data["datasets"]
assert isinstance(DATASET_SOURCES, dict)
assert (SERIALIZATION_FORMATS := tuple(config_data["formats"]))
OUT_PATH = Path(config_data.get("outdir", "./datasets"))
TEMP_PATH = Path(config_data.get("tempdir", "./temp"))
DATASET_NDJSON_PATH = OUT_PATH / "dataset.ndjson"
DATASET_SQLITE_PATH = OUT_PATH / "dataset.sqlite"
INIT_DB_PATH = Path("init.sql")
