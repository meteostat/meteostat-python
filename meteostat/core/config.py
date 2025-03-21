import os
import json
from dataclasses import fields

from meteostat.core.logger import logger


class ConfigService:
    """
    Config Service

    An abstract class which provides configuration-related methods.
    """

    @property
    def _field_names(self) -> dict:
        """
        A dictionary mapping each dataclass field to its type
        """
        return {f.name: f.type for f in fields(self)}

    def set(self, key: str, value: str) -> None:
        """
        Set a configuration using a key-value pair
        """
        if key in self._field_names:
            try:
                parsed_value = json.loads(value)
                expected_type = self._field_names[key]
                setattr(self, key, expected_type(parsed_value))
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Failed to parse environment variable '{key}'")
        else:
            logger.warning(
                f"Environment variable '{key}' does not exist in configuration and will be ignored"
            )

    def load_env(self, prefix="MS") -> None:
        """
        Update configuration from environment variables with a given prefix.
        """
        prefix = f"{prefix}_" if prefix else ""

        for key, value in os.environ.items():
            # Skip if key doesn't start with prefix
            if not key.startswith(prefix):
                continue

            # Remove prefix and match with dataclass fields
            key = key.replace(prefix, "").lower()

            self.set(key, value)
