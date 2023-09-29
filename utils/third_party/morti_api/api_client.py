import asyncio

import httpx as httpx
from typing import List

from models.models import ProcessedData


class RickAndMortyApiClient:
    BASE_URL = "https://rickandmortyapi.com/api/"
    ENDPOINTS = ["character", "location", "episode"]

    @classmethod
    async def fetch_data(cls, endpoint: str) -> List[ProcessedData]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{cls.BASE_URL}/{endpoint}")
            response_data = response.json()

            total_pages = response_data["info"]["pages"]
            all_data = response_data["results"]

            async def fetch_page(page: int):
                res = await client.get(f"{cls.BASE_URL}/{endpoint}?page={page}")
                all_data.extend(res.json()["results"])

            if total_pages > 1:
                await asyncio.gather(*(fetch_page(page) for page in range(2, total_pages + 1)))

            return [ProcessedData(
                Id=str(item["id"]),
                Metadata=item["name"],
                RawData=item
            ) for item in all_data]
