from os import sep
from os.path import expanduser

_METEOSTAT_DIR = expanduser("~") + sep + ".meteostat"

DEFAULT_SETTINGS = {
    "debug": False,
    "max_workers": 12,
    "meteostat_dir": _METEOSTAT_DIR,
    "cache_dir": lambda: _METEOSTAT_DIR + sep + "cache",
    "log_file": lambda: _METEOSTAT_DIR + sep + "debug.log",
    "cache_enable": True,
    "cache_max_age": 60*60*24*30, # 30 days
    "cache_autoclean": True,
    "stations_meta_mirrors": [
            'https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json'
    ],
    "noaa_isd_lite_endpoint": 'https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/'
}