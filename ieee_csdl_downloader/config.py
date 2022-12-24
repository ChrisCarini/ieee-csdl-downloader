import functools

from pathlib import Path

import yaml


@functools.lru_cache(maxsize=None)
def get_config():  # pragma: nocover
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config


def debug_mode():  # pragma: nocover
    return get_config().get('DEBUG', False)


def get_download_start_year():  # pragma: nocover
    return get_config().get('DOWNLOAD_START_YEAR', None)


def get_download_dir():  # pragma: nocover
    return Path(get_config().get('DOWNLOAD_DIR'))


def get_publications():  # pragma: nocover
    return get_config().get('PUBLICATIONS')


def get_ieee_csdl_cookies():  # pragma: nocover
    return {
        'CSDL_AUTH_COOKIE': get_config().get('CSDL_AUTH_COOKIE'),
    }


def get_ieee_spectrum_cookies():  # pragma: nocover
    return {
        'sessionid': get_config().get('IEEE_SPECTRUM_SESSIONID'),
    }
