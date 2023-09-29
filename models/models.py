from pydantic import BaseModel
from typing import List, Dict, Any


class ProcessedData(BaseModel):
    Id: str
    Metadata: str
    RawData: Dict[str, Any]


class FilteredData(BaseModel):
    episodes_filtered: List[Any]
    locations_filtered: List[Any]
