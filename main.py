import asyncio
from typing import List, Tuple

from fastapi import FastAPI

from models.models import FilteredData
from utils.third_party.morti_api.api_client import RickAndMortyApiClient
from utils.business_logic import filter_data, write_json_files

app = FastAPI(debug=True)


@app.get("/", response_model=FilteredData)
async def read_morti_api_content():
    all_data = await asyncio.gather(
        *(RickAndMortyApiClient.fetch_data(endpoint) for endpoint in RickAndMortyApiClient.ENDPOINTS))

    combined_filtered_data = FilteredData(episodes_filtered=[], locations_filtered=[])

    for i, endpoint_data in enumerate(all_data):
        write_json_files(RickAndMortyApiClient.ENDPOINTS[i], endpoint_data)

        episodes_filtered, locations_filtered = filter_data(endpoint_data, RickAndMortyApiClient.ENDPOINTS[i])

        combined_filtered_data.episodes_filtered.extend(episodes_filtered)
        combined_filtered_data.locations_filtered.extend(locations_filtered)

    return combined_filtered_data
