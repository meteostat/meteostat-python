from meteostat import types
from meteostat.enumerations import Interface, Parameter, Provider


PROVIDERS: list[types.Provider] = [
    {
        'id': Provider.DWD_CLIMATE_HOURLY,
        'name': 'DWD Climate Hourly',
        'interface': Interface.HOURLY,
        'countries': ['DE'],
        'parameters': [
            Parameter.TEMP,
            Parameter.PRCP,
            Parameter.WDIR            
        ],
        'license': 'https://www.dwd.de/DE/service/copyright/copyright_node.html',
        'module': 'meteostat.providers.dwd.climate_hourly'
    },
    {
        'id': Provider.DWD_CLIMATE_DAILY,
        'name': 'DWD Climate Daily',
        'interface': Interface.DAILY,
        'countries': ['DE'],
        'parameters': [
            Parameter.TEMP,
            Parameter.PRCP,
            Parameter.WDIR            
        ],
        'license': 'https://www.dwd.de/DE/service/copyright/copyright_node.html',
        'module': 'meteostat.providers.dwd.climate_daily'
    },
    {
        'id': Provider.NOAA_ISD_LITE,
        'name': 'NOAA ISD Lite',
        'interface': Interface.HOURLY,
        'countries': ['DE'],
        'parameters': [
            Parameter.TEMP,
            Parameter.PRCP,
            Parameter.WDIR            
        ],
        'module': 'meteostat.providers.noaa.isd_lite'
    },
    {
        'id': Provider.NOAA_GHCND,
        'name': 'NOAA GHCN Daily',
        'interface': Interface.HOURLY,
        'countries': ['DE'],
        'parameters': [
            Parameter.TEMP,
            Parameter.PRCP,
            Parameter.WDIR            
        ],
        'module': 'meteostat.providers.noaa.ghcnd'
    }
]