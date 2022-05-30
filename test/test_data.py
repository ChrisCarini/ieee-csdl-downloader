import pytest

from ieee_csdl_downloader.download import get_pub_formats, get_pub_month


@pytest.mark.parametrize(
    'json_data, expected',
    [
        # empty in, empty out
        ({}, set()),
        ({'data': {}}, set()),
        ({'data': {'issue': {}}}, set()),
        # Single file
        ({'data': {'issue': {'downloadables': {'hasEpub': True}}}}, {'epub'}),
        ({'data': {'issue': {'downloadables': {'hasMobi': True}}}}, {'mobi'}),
        ({'data': {'issue': {'downloadables': {'hasPdf': True}}}}, {'pdf'}),
        ({'data': {'issue': {'downloadables': {'hasZip': True}}}}, {'zip'}),
        # Double files
        ({'data': {'issue': {'downloadables': {'hasEpub': True, 'hasMobi': True}}}}, {'epub', 'mobi'}),
        ({'data': {'issue': {'downloadables': {'hasPdf': True, 'hasZip': True}}}}, {'pdf', 'zip'}),
        # All the files
        ({'data': {'issue': {'downloadables': {'hasEpub': True, 'hasMobi': True, 'hasPdf': True, 'hasZip': True}}}}, {'epub', 'mobi', 'pdf', 'zip'}),
        # All the entries, none of the files
        ({'data': {'issue': {'downloadables': {'hasEpub': False, 'hasMobi': False, 'hasPdf': False, 'hasZip': False}}}}, set()),
        # All the entries, half the files
        ({'data': {'issue': {'downloadables': {'hasEpub': True, 'hasMobi': False, 'hasPdf': True, 'hasZip': False}}}}, {'epub', 'pdf'}),
        ({'data': {'issue': {'downloadables': {'hasEpub': False, 'hasMobi': True, 'hasPdf': False, 'hasZip': True}}}}, {'mobi', 'zip'}),
    ],
)
def test_get_pub_formats(json_data, expected) -> None:
    # when
    result = get_pub_formats(json_data)

    # then
    assert result == expected


@pytest.mark.parametrize(
    'json_data, expected',
    [
        # empty in, empty out
        ({}, None),
        ({'data': {}}, None),
        ({'data': {'issue': {}}}, None),
        ({'data': {'issue': {'label': None}}}, None),
        # with label
        ({'data': {'issue': {'label': 'January'}}}, 1),
        ({'data': {'issue': {'label': 'February'}}}, 2),
        ({'data': {'issue': {'label': 'March'}}}, 3),
        ({'data': {'issue': {'label': 'April'}}}, 4),
        ({'data': {'issue': {'label': 'May'}}}, 5),
        ({'data': {'issue': {'label': 'June'}}}, 6),
        ({'data': {'issue': {'label': 'July'}}}, 7),
        ({'data': {'issue': {'label': 'August'}}}, 8),
        ({'data': {'issue': {'label': 'September'}}}, 9),
        ({'data': {'issue': {'label': 'October'}}}, 10),
        ({'data': {'issue': {'label': 'November'}}}, 11),
        ({'data': {'issue': {'label': 'December'}}}, 12),
        # ending with dot
        ({'data': {'issue': {'label': 'Jan.'}}}, 1),
    ],
)
def test_get_pub_month(json_data, expected) -> None:
    # when
    result = get_pub_month(json_data)

    # then
    assert result == expected
