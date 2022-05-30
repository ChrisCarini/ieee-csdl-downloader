import functools

import yaml


@functools.lru_cache(maxsize=None)
def get_config():
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config
