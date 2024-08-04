import json
from meteostat.settings import settings, env


def test_env(monkeypatch):
    """
    It should load values from environment variables
    """
    # Set environment variables
    monkeypatch.setenv("MS_CACHE_ENABLE", json.dumps(False))
    monkeypatch.setenv("MS_CACHE_TTL_MAX", json.dumps(10))

    # Load environment variables into settings
    env()

    # Check that the values have been updated
    assert settings["cache_enable"] is False
    assert settings["cache_ttl_max"] == 10

    # Test with a different prefix
    monkeypatch.setenv("OTHER_PREFIX_CACHE_ENABLE", json.dumps(True))
    env("OTHER_PREFIX")
    assert settings["cache_enable"] is True
