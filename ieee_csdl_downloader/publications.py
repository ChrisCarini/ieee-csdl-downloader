from dataclasses import dataclass, field
from typing import List, Optional

from ieee_csdl_downloader.config import get_config


@dataclass
class Publication:
    name: str
    type: str
    url_indicator: str
    start_year: int
    end_year: Optional[int]
    issues: List[int] = field(default_factory=list)

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
                    issues=[x.strip() for x in publication.get('issues', '1, 2, 3, 4, 5, 6').split(',')],
                )
            )

        return result
