import requests

from meteostat.configuration import config


class NetworkService:
    """
    Network Service
    """

    @staticmethod
    def get(url: str, params=None, headers=None) -> requests.Response:
        """
        Send a GET request using the Meteostat configuration
        """

        return requests.get(url, params, headers=headers, proxies=config.proxies)


network_service = NetworkService()
