from ieee_csdl_downloader.config import get_config

COOKIES = {
    'CSDL_AUTH_COOKIE': get_config().get('CSDL_AUTH_COOKIE'),
}
