from meteostat.utilities.endpoint import generate_endpoint_path
from meteostat.enumerations.granularity import Granularity
from datetime import datetime


def test_generate_endpoint_path_normals():
    assert "normals/10286.csv.gz" == generate_endpoint_path(1, 2, Granularity.NORMALS, '10286')

def test_generate_endpoint_path_hourly_full():
    assert "hourly/full/10286.csv.gz" == generate_endpoint_path(datetime(2020, 1, 1), datetime(2021, 10, 1), Granularity.HOURLY, '10286')

def test_generate_endpoint_path_hourly_full_obs():
    assert "hourly/obs/10286.csv.gz" == generate_endpoint_path(datetime(2020, 1, 1), datetime(2021, 10, 1), Granularity.HOURLY, '10286', True)

def test_generate_endpoint_path_hourly_subset():
    assert "hourly/2021/10286.csv.gz" == generate_endpoint_path(datetime(2021, 1, 1), datetime(2021, 10, 1), Granularity.HOURLY, '10286')

def test_generate_endpoint_path_daily_subset():
    assert "daily/full/10286.csv.gz" == generate_endpoint_path(datetime(2021, 1, 1), datetime(2021, 10, 1), Granularity.DAILY, '10286')

def test_generate_endpoint_path_monthly_subset():
    assert "monthly/full/10286.csv.gz" == generate_endpoint_path(datetime(2021, 1, 1), datetime(2021, 10, 1), Granularity.MONTHLY, '10286')
