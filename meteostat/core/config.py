import os
import json
from typing import Any, Optional

from meteostat.core.logger import logger


class ConfigService:
    prefix = "MS"

    _namespace: Optional[str]
    _config: dict[str, Any]

    def __init__(
        self, namespace: Optional[str] = None, root_config: dict[str, Any] = {}
    ):
        self._namespace = namespace
        self._config = root_config

    def _get_key(self, key: str) -> str:
        """
        Get a configuration key with optional namespace
        """
        key = key.replace(".", "__")
        if self._namespace:
            key = f"{self._namespace}__{key}"
        return key

    def _parse_env_value(self, key: str, value: str) -> Any:
        """
        Parse an environment variable value
        """
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError, ValueError):
            logger.error(f"Failed to parse environment variable '{key}'")
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration using a key-value pair
        """
        key = self._get_key(key)
        self._config[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value by key
        """
        key = self._get_key(key)
        return self._config.get(key, default)

    def get_env_name(self, key: str) -> str:
        """
        Get the environment variable name for a given key
        """
        prefix = f"{self.prefix}__" if self.prefix else ""
        key = f"{prefix}{self._get_key(key)}"
        return key.upper()

    def load_env(self) -> None:
        """
        Update configuration from environment variables with a given prefix.
        """
        prefix = f"{self.prefix}__" if prefix else ""

        for key, value in os.environ.items():
            if not key.startswith(prefix):
                continue

            key = key.replace(prefix, "").lower()
            value = self._parse_env_value(key, value)

            if value is not None:
                self.set(key, value)

    def __getitem__(self, namespace: str) -> "ConfigService":
        """
        Return a new ConfigService instance scoped to the given namespace.
        """
        if self._namespace:
            namespace = f"{self._namespace}__{namespace}"
        return ConfigService(namespace, self._config)

    def __repr__(self) -> str:
        """
        Return a formatted representation of the configuration
        """

        def nest_dict(keys, value, d):
            if len(keys) == 1:
                d[keys[0]] = value
            else:
                d.setdefault(keys[0], {})
                nest_dict(keys[1:], value, d[keys[0]])

        nested_config = {}
        for key, value in self._config.items():
            keys = key.split("__")
            nest_dict(keys, value, nested_config)

        def format_nested(d, indent=0):
            result = ""
            for k, v in d.items():
                if isinstance(v, dict):
                    result += "  " * indent + k + "\n" + format_nested(v, indent + 1)
                else:
                    result += "  " * indent + f"{k} = {repr(v)}\n"
            return result

        return format_nested(nested_config).strip()


config = ConfigService()
