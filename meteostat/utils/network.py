import requests

from meteostat.settings import settings


def get(url: str, params = None, headers = None) -> requests.Response:
    return requests.get(url, params, headers=headers, proxies=settings['proxies'])