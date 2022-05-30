from dataclasses import dataclass
from typing import Optional


@dataclass
class Publication:
    name: str
    type: str
    url_indicator: str
    start_year: int
    end_year: Optional[int]
