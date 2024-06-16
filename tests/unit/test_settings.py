import pytest
import json
from meteostat.settings import Settings


def test_set_value():
    """
    It should set the value for valid keys and raise an exception
    for invalid keys
    """
    Settings.set_value("cache_enable", False)
    assert Settings.cache_enable is False

    Settings.set_value("cache_ttl_max", 60 * 60 * 24 * 60)  # 60 days
    assert Settings.cache_ttl_max == 60 * 60 * 24 * 60

    with pytest.raises(AttributeError):
        Settings.set_value("nonexistent_attribute", "some_value")


def test_load_env(monkeypatch):
    """
    It should load values from environment variables
    """
    # Set environment variables
    monkeypatch.setenv("MS_CACHE_ENABLE", json.dumps(False))
    monkeypatch.setenv("MS_REQUEST_TIMEOUT", json.dumps(10))

    # Load environment variables into settings
    Settings.load_env("MS")

    # Check that the values have been updated
    assert Settings.cache_enable is False
    assert Settings.request_timeout == 10

    # Test with a different prefix
    monkeypatch.setenv("OTHER_PREFIX_CACHE_ENABLE", json.dumps(True))
    Settings.load_env("OTHER_PREFIX")
    assert Settings.cache_enable is True
