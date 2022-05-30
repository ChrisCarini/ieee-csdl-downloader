from datetime import datetime
from typing import Optional, Set


def get_pub_formats(json_data: dict) -> Set[str]:
    formats: Set[str] = set()
    data = json_data.get('data', None)
    if not data:
        return formats
    issue = data.get('issue', None)
    if not issue:
        return formats
    downloadables = issue.get('downloadables', {})

    if downloadables.get('hasEpub'):
        formats.add('epub')
    if downloadables.get('hasMobi'):
        formats.add('mobi')
    if downloadables.get('hasPdf'):
        formats.add('pdf')
    if downloadables.get('hasZip'):
        formats.add('zip')

    return formats


def _extract_month_number(pub_month: str) -> int:
    if pub_month.endswith('.'):
        pub_month = pub_month[:-1]
    if len(pub_month) > 3:
        pub_month = pub_month[:3]
    mm = None
    try:
        mm = datetime.strptime(pub_month, '%B')
    except Exception:
        mm = datetime.strptime(pub_month, '%b')
    return mm.month


def get_pub_month(json_data: dict) -> Optional[int]:
    data = json_data.get('data', None)
    if not data:
        return None
    issue = data.get('issue', None)
    if not issue:
        return None
    label = issue.get('label', None)
    if not label:
        return None

    pub_month = _extract_month_number(label)
    return pub_month
