from pathlib import Path
from typing import Any
import json
import logging

#### setting up logger ####
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def load_json(file_path: Path) -> Any:
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        logger.exception("Error trying to load json file from %s", file_path)
        raise e


def save_json(data: Any, file_path: Path, indent=2, sort_keys=False) -> bool:

    try:
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=indent, sort_keys=sort_keys)
        return True
    except Exception as e:
        logger.exception("Error trying to save json data to %s", file_path)
        raise e
