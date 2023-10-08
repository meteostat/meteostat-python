import json
from typing import Any
from os import environ
from meteostat.config.settings import DEFAULT_SETTINGS

class _Setting:
    env_prefix = ''
    _defaults = {}
    _overrides = {}

    def __init__(self, default_settings: dict = {}, env_prefix = 'MS'):
        for key, value in default_settings.items():
            self.add(key, value)
        self.__dict__['env_prefix'] = env_prefix

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self._defaults:
            self.set(key, value)
        else:
            self.add(key, value)

    def __getattr__(self, key: str) -> Any:
        return self.get(key)

    def add(self, key: str, value: Any):
        self._defaults[key] = value

    def set(self, key: str, value: Any):
        if key in self._defaults:
            self._overrides[key] = value
        else:
            raise Exception(f'Key "{key}" does not exist')

    def get(self, key: str):
        if key in self._overrides:
            value = self._overrides[key]
            return value() if callable(value) else value
        env_key = f'{self.env_prefix}_{key.upper()}'
        if env_key in environ:
            try:
                return json.loads(environ.get(env_key))
            except json.JSONDecodeError:
                return environ.get(env_key)
        value = self._defaults[key]
        return value() if callable(value) else value
    
    def reset(self) -> None:
        self._overrides.clear()
    
settings = _Setting(DEFAULT_SETTINGS)