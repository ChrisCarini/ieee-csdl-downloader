from pathlib import Path

from ieee_csdl_downloader.download import build_download_url, get_local_filename, get_publication_directory
from ieee_csdl_downloader.publications import Publication


def test_get_publication_directory() -> None:
    # given
    name = 'foobar'

    # when
    result = get_publication_directory(name)

    # then
    assert result == Path('downloads/foobar')


def test_get_local_filename() -> None:
    # when
    result = get_local_filename(2022, '05', 'pub_name', '123', 456, 'pdf')

    # then
    assert result == Path('downloads/pub_name/2022-05 - pub_name - Volume123 - Issue456.pdf')

    # when
    result = get_local_filename(2022, '05', 'pub_name', '123', 456, 'pdf', postfix='POSTFIX')

    # then
    assert result == Path('downloads/pub_name/2022-05 - pub_name - Volume123 - Issue456POSTFIX.pdf')


def test_build_download_url() -> None:  # pub, year, issue, filetype):
    # given
    pub = Publication(name='IEEE Security & Privacy', type='mags', url_indicator='sp', start_year=2003, end_year=None)

    # when
    result = build_download_url(pub=pub, year=2022, issue=4, filetype='pdf')

    # then
    assert result == 'https://www.computer.org/csdl/api/v1/periodical/mags/sp/2022/04/download-issue/pdf'
