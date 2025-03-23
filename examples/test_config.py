import os
import json
from typing import Any, Optional


class ConfigService:
    _namespace: Optional[str]
    _config: dict

    def __init__(
        self,
        namespace: Optional[str] = None,
        base_config={},
    ):
        self._namespace = namespace
        self._config = base_config

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

    def get_env_name(self, key: str, prefix: Optional[str] = "MS") -> str:
        """
        Get the environment variable name for a given key
        """
        prefix = f"{prefix}__" if prefix else ""
        key = f"{prefix}{self._get_key(key)}"
        return key.upper()

    def load_env(self, prefix: Optional[str] = "MS") -> None:
        """
        Update configuration from environment variables with a given prefix.
        """
        prefix = f"{prefix}_" if prefix else ""

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


config = ConfigService()


cnf = config["user"]["data"]

cnf.set("agent", "myapp")
print(cnf.get("agent"))
print(config.get("user.data.agent"))
