from dataclasses import dataclass
from typing import List, Optional

from ieee_csdl_downloader.config import get_config


@dataclass
class Publication:
    name: str
    type: str
    url_indicator: str
    start_year: int
    end_year: Optional[int]

    @classmethod
    def from_config(cls) -> List['Publication']:
        result: List[Publication] = []
        for publication in get_config().get('PUBLICATIONS'):
            result.append(
                Publication(
                    name=publication.get('name'),
                    type=publication.get('type'),
                    url_indicator=publication.get('url_indicator'),
                    start_year=publication.get('start_year'),
                    end_year=publication.get('end_year', None),
                )
            )

        return result
