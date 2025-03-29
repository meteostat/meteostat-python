"""
Network Service

The Network Service provides methods to send HTTP requests
considering the Meteostat configuration.
"""

from typing import Optional
import requests

from meteostat import __version__
from meteostat.core.config import config


class NetworkService:
    """
    Network Service
    """

    @staticmethod
    def _process_headers(headers: dict) -> dict:
        """
        Process headers
        """

        headers["X-Meteostat-Version"] = __version__

        return headers

    def get(
        self, url: str, params=None, headers: dict = {}, stream: Optional[bool] = None
    ) -> requests.Response:
        """
        Send a GET request using the Meteostat configuration
        """

        headers = self._process_headers(headers)

        return requests.get(
            url,
            params,
            headers=headers,
            stream=stream,
            proxies=config.get("network.proxies"),
        )


network_service = NetworkService()
