from pathlib import Path
from unittest import mock

import pytest
import yaml

import ieee_csdl_downloader.config


def get_test_config():
    with open(Path(__file__).parent / 'resources/config_test_file.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config


@pytest.fixture(scope='session', autouse=True)
def my_thing_mock():
    with mock.patch.object(ieee_csdl_downloader.config, 'get_config', get_test_config):
        yield
