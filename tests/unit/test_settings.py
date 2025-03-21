import json
from meteostat.configuration import config


def test_env(monkeypatch):
    """
    It should load values from environment variables
    """
    # Set environment variables
    monkeypatch.setenv("MS_CACHE_ENABLE", json.dumps(False))
    monkeypatch.setenv("MS_CACHE_TTL", json.dumps(10))

    # Load environment variables into settings
    config.parse_env()

    # Check that the values have been updated
    assert config.cache_enable is False
    assert config.cache_ttl == 10

    # Test with a different prefix
    monkeypatch.setenv("OTHER_PREFIX_CACHE_ENABLE", json.dumps(True))
    config.parse_env("OTHER_PREFIX")
    assert config.cache_enable is True
