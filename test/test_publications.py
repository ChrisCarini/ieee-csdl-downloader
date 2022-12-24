from ieee_csdl_downloader.publications import Publication


def test_from_config() -> None:
    # when
    result = Publication.from_config()

    # then
    assert isinstance(result, list)
    assert len(result) == 7, 'There are 7 publications in the sample test config file.'
