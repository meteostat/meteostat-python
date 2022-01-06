from meteostat.core.cache import get_local_file_path

expected_file_path = "cache/hourly/6dfc35c47756e962ef055d1049f1f8ec"

def test_get_local_file_path():
    assert get_local_file_path("cache", "hourly", '10101') == expected_file_path

def test_get_local_file_path_chunked():
    assert get_local_file_path("cache", "hourly", '10101_2022') != expected_file_path
