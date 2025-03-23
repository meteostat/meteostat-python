"""
Network Service

The Network Service provides methods to send HTTP requests
considering the Meteostat configuration.
"""

import requests

from meteostat.core.config import config


class NetworkService:
    """
    Network Service
    """

    @staticmethod
    def get(url: str, params=None, headers=None) -> requests.Response:
        """
        Send a GET request using the Meteostat configuration
        """

        return requests.get(
            url, params, headers=headers, proxies=config.get("network.proxies")
        )


network_service = NetworkService()
