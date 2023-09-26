import os

class DefaultConfig:
    debug = False
    meteostat_dir = os.path.expanduser("~") + os.sep + ".meteostat"
    cache_dir = meteostat_dir + os.sep + "cache"
    log_file = meteostat_dir + os.sep + 'debug.log'
    max_workers = 12
    cache_enable = True
    cache_max_age = 60*60*24*30 # 30 days
    cache_autoclean = True
    stations_meta_mirrors = [
        'https://raw.githubusercontent.com/meteostat/weather-stations/master/stations/{id}.json'
    ]