import os
import time
from unittest import mock
import pandas as pd
from meteostat.cache import (
    create_cache_dir,
    fetch,
    persist,
    purge,
    write_json,
    write_pickle,
    read_pickle,
    func_to_uid,
    get_cache_path,
    is_stale,
)
from meteostat.typing import SettingsDict


MODULE_PATH = "meteostat.cache"


settings: SettingsDict = {
    "cache_dir": "meteostat/cache",
    "cache_ttl_min": 10,
    "cache_ttl_max": 100,
}


def test_create_cache_dir(mocker):
    mock_exists = mocker.patch(f"{MODULE_PATH}.os.path.exists", return_value=False)
    mock_makedirs = mocker.patch(f"{MODULE_PATH}.os.makedirs")
    mocker.patch(f"{MODULE_PATH}.settings", settings)

    # It should create the cache directory if it doesn't exist
    create_cache_dir()
    mock_makedirs.assert_called_once_with(settings["cache_dir"])

    mock_makedirs.reset_mock()

    # It should not attempt to create the cache directory if it already exists
    mock_exists.return_value = True
    create_cache_dir()
    mock_makedirs.assert_not_called()


def test_write_pickle(mocker):
    mock_to_pickle = mocker.patch(f"{MODULE_PATH}.pd.DataFrame.to_pickle")

    # It creates a Pickle file if df is None
    test_path = "test_path_none"
    write_pickle(test_path, None)
    mock_to_pickle.assert_called_once_with(test_path)

    mock_to_pickle.reset_mock()

    # It creates a Pickle file if df is given
    test_path = "test_path_df"
    test_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    write_pickle(test_path, test_df)
    test_df.to_pickle.assert_called_once_with(test_path)


def test_read_pickle(mocker):
    mock_read_pickle = mocker.patch(f"{MODULE_PATH}.pd.read_pickle")

    # It should return None if DataFrame is empty
    test_path_empty = "test_path_empty"
    mock_read_pickle.return_value = pd.DataFrame()
    result = read_pickle(test_path_empty)
    mock_read_pickle.assert_called_once_with(test_path_empty)
    assert result is None

    mock_read_pickle.reset_mock()

    # It should return the DataFrame
    test_path_non_empty = "test_path_non_empty"
    test_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    mock_read_pickle.return_value = test_df
    result = read_pickle(test_path_non_empty)
    mock_read_pickle.assert_called_once_with(test_path_non_empty)
    assert result is test_df


def test_write_json(mocker):
    mock_open = mocker.patch("builtins.open", mock.mock_open())
    test_path = "test_path"
    test_data_dict = {"key": "value"}
    test_data_list = ["item1", "item2"]
    mock_json_dump = mocker.patch(f"{MODULE_PATH}.json.dump")

    # It should save a dictionary
    write_json(test_path, test_data_dict)
    mock_open.assert_called_once_with(test_path, "w")
    mock_json_dump.assert_called_once_with(test_data_dict, mock_open())

    mock_open.reset_mock()
    mock_json_dump.reset_mock()

    # It should save a list
    write_json(test_path, test_data_list)
    mock_open.assert_called_once_with(test_path, "w")
    mock_json_dump.assert_called_once_with(test_data_list, mock_open())


def test_persist(mocker):
    # Mock the create_cache_dir, write_json, and write_pickle functions
    mock_create_cache_dir = mocker.patch(f"{MODULE_PATH}.create_cache_dir")
    mock_write_json = mocker.patch(f"{MODULE_PATH}.write_json")
    mock_write_pickle = mocker.patch(f"{MODULE_PATH}.write_pickle")

    # Define test path and data
    test_path = "test_path"
    test_data_dict = {"key": "value"}
    test_data_list = ["item1", "item2"]
    test_data_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    # Test case for JSON data (dictionary)
    persist(test_path, test_data_dict, "json")
    mock_create_cache_dir.assert_called_once()
    mock_write_json.assert_called_once_with(test_path, test_data_dict)
    mock_write_pickle.assert_not_called()

    # Reset mocks
    mock_create_cache_dir.reset_mock()
    mock_write_json.reset_mock()
    mock_write_pickle.reset_mock()

    # Test case for JSON data (list)
    persist(test_path, test_data_list, "json")
    mock_create_cache_dir.assert_called_once()
    mock_write_json.assert_called_once_with(test_path, test_data_list)
    mock_write_pickle.assert_not_called()

    # Reset mocks
    mock_create_cache_dir.reset_mock()
    mock_write_json.reset_mock()
    mock_write_pickle.reset_mock()

    # Test case for pickle data (DataFrame)
    persist(test_path, test_data_df, "pickle")
    mock_create_cache_dir.assert_called_once()
    mock_write_pickle.assert_called_once_with(test_path, test_data_df)
    mock_write_json.assert_not_called()


def test_fetch(mocker):
    # Mock the read_json and read_pickle functions
    mock_read_json = mocker.patch(f"{MODULE_PATH}.read_json")
    mock_read_pickle = mocker.patch(f"{MODULE_PATH}.read_pickle")

    # Define test path and expected data
    test_path = "test_path"
    expected_data_dict = {"key": "value"}
    expected_data_list = ["item1", "item2"]
    expected_data_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    # Test case for JSON data (dictionary)
    mock_read_json.return_value = expected_data_dict
    result = fetch(test_path, "json")
    mock_read_json.assert_called_once_with(test_path)
    mock_read_pickle.assert_not_called()
    assert result == expected_data_dict

    # Reset mocks
    mock_read_json.reset_mock()
    mock_read_pickle.reset_mock()

    # Test case for JSON data (list)
    mock_read_json.return_value = expected_data_list
    result = fetch(test_path, "json")
    mock_read_json.assert_called_once_with(test_path)
    mock_read_pickle.assert_not_called()
    assert result == expected_data_list

    # Reset mocks
    mock_read_json.reset_mock()
    mock_read_pickle.reset_mock()

    # Test case for pickle data (DataFrame)
    mock_read_pickle.return_value = expected_data_df
    result = fetch(test_path, "pickle")
    mock_read_pickle.assert_called_once_with(test_path)
    mock_read_json.assert_not_called()
    assert result.equals(expected_data_df)


def test_func_to_uid():
    def say_hello(name: str):
        return f"Hello {name}"

    assert func_to_uid(say_hello, "World", {}) == "bceb5d5d6f7d70f7d90565f242c92c22"


def test_get_cache_path(mocker):
    mocker.patch(f"{MODULE_PATH}.settings", settings)

    assert get_cache_path("abc", "json") == "meteostat/cache/abc.json"


def test_is_stale(mocker):
    test_path = "test_path"
    test_ttl = 50

    mocker.patch("os.path.getmtime", return_value=1000)
    mocker.patch("time.time", return_value=2000)
    mocker.patch(f"{MODULE_PATH}.settings", settings)

    expected_ttl = min(
        max(test_ttl, settings["cache_ttl_min"]), settings["cache_ttl_max"]
    )

    assert is_stale(test_path, test_ttl) == (2000 - 1000 > expected_ttl)

    mocker.patch("os.path.getmtime", return_value=1500)
    mocker.patch("time.time", return_value=1600)

    # Check if the file is stale
    assert is_stale(test_path, test_ttl) == (1600 - 1500 > expected_ttl)


def test_purge(mocker):
    mock_logger = mocker.patch(f"{MODULE_PATH}.logger")
    mock_exists = mocker.patch(f"{MODULE_PATH}.os.path.exists", return_value=True)
    mock_listdir = mocker.patch(
        f"{MODULE_PATH}.os.listdir", return_value=["file1", "file2"]
    )
    mock_getmtime = mocker.patch(
        f"{MODULE_PATH}.os.path.getmtime",
        side_effect=[time.time() - 150, time.time() - 50],
    )
    mock_isfile = mocker.patch(f"{MODULE_PATH}.os.path.isfile", return_value=True)
    mock_remove = mocker.patch(f"{MODULE_PATH}.os.remove")
    mocker.patch(f"{MODULE_PATH}.settings", settings)

    # Test purge with default TTL (settings["cache_ttl_max"])
    purge()
    mock_logger.info.assert_called_once_with(
        f"Removing cached files older than {settings['cache_ttl_max']} seconds"
    )

    # Assert os.remove was called for the file older than TTL
    mock_remove.assert_called_once_with(os.path.join(settings["cache_dir"], "file1"))

    # Reset mocks
    mock_logger.reset_mock()
    mock_exists.reset_mock()
    mock_listdir.reset_mock()
    mock_getmtime.reset_mock()
    mock_isfile.reset_mock()
    mock_remove.reset_mock()

    # Mock os.path.getmtime to return different times
    mock_getmtime.side_effect = [time.time() - 200, time.time() - 50]

    # Test purge with a specific TTL
    purge(ttl=150)
    mock_logger.info.assert_called_once_with(
        "Removing cached files older than 150 seconds"
    )

    # Assert os.remove was called for the file older than TTL
    mock_remove.assert_called_once_with(os.path.join(settings["cache_dir"], "file1"))

    # Ensure os.remove was not called for the file not older than TTL
    mock_remove.assert_called_once()  # This checks if it was called only once in total
