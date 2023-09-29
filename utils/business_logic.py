import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from models.models import ProcessedData

DEFAULT_OUTPUT_DIR = Path("utils") / "third_party" / "morti_api" / "json_output"


def filter_data(all_data: List[ProcessedData], endpoint: str) -> Tuple[List[str], List[str]]:
    """
    Filter fetched data based on the endpoint and specific criteria.

    :param all_data: A list of ProcessedData objects to be filtered.
    :param endpoint: The endpoint for which data has been fetched.
    :return: A tuple containing lists of filtered episodes and locations.
    """
    episodes_filtered = []
    locations_filtered = []

    if endpoint == "episode":
        for data in all_data:
            raw_data = data.RawData
            air_date = datetime.strptime(raw_data.get("air_date"), "%B %d, %Y")
            if 2017 <= air_date.year <= 2021 and len(raw_data.get("characters", [])) > 3:
                episodes_filtered.append(raw_data.get("name"))

    elif endpoint == "location":
        for data in all_data:
            raw_data = data.RawData
            episodes = [int(ep.split("/")[-1]) for ep in raw_data.get("episode", [])]
            if all(ep % 2 != 0 for ep in episodes):
                locations_filtered.append(raw_data.get("name"))

    return episodes_filtered, locations_filtered


def write_json_files(endpoint: str, all_data: List[ProcessedData], output_dir: Path = DEFAULT_OUTPUT_DIR):
    """
    Write the fetched data to JSON files in the specified output directory.

    :param endpoint: The endpoint for which data has been fetched.
    :param all_data: A list of ProcessedData objects to be written to JSON files.
    :param output_dir: The directory where the JSON files will be created.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"{endpoint}_{timestamp}.json"

    output_data = [data.dict() for data in all_data]
    with file_path.open('w') as f:
        json.dump(output_data, f, indent=2)
