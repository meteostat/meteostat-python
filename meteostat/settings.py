import os
import json

from meteostat.typing import SettingsDict


settings: SettingsDict = {
    "cache_enable": True,
    "cache_dir": os.path.expanduser("~") + os.sep + ".meteostat" + os.sep + "cache",
    "cache_ttl_max": 60 * 60 * 24 * 30,
    "cache_ttl_min": 0,
    "cache_autoclean": True,
    "load_sources": False,
    "point_radius": 50000,
    "point_stations": 4,
    "proxies": None,
    "provider_metno_user_agent": None  # User-Agent required for MET Norway (https://api.met.no/doc/TermsOfService)
}


def env(prefix="MS") -> None:
    """
    Import configuration from environment variables
    """
    prefix = f"{prefix}_" if prefix else None
    for key, value in os.environ.items():
        if prefix and not key.startswith(prefix):
            continue
        key = key.replace(prefix, "").lower()
        value = json.loads(value)
        if key in settings:
            value_type = type(settings[key])
            settings[key] = value_type(value)
        else:
            raise KeyError(f"Unsupported settings key '{key}'")
