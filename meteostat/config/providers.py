from meteostat import types
from meteostat.enumerations import Interface, Parameter, Provider


DEFAULT_PROVIDERS: list[types.Provider] = [
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
        'handler': 'meteostat.provider.noaa.isd_lite'
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
        'handler': 'meteostat.provider.noaa.isd_lite'
    }
]