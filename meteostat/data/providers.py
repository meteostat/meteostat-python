from meteostat import Providers, Parameters, framework

DEFAULT_PROVIDERS: list[framework.Provider] = [
    framework.Provider(
        id=Providers.DWD_CLIMATE_HOURLY,
        name='DWD Climate Hourly',
        countries=[
            'DE'
        ],
        parameters=[
            Parameters.TEMP,
            Parameters.PRCP,
            Parameters.WDIR
        ],
        license='https://www.dwd.de/DE/service/copyright/copyright_node.html',
        handler='meteostat.provider.dwd.climate_hourly'
    ),
    framework.Provider(
        id=Providers.NOAA_ISD_LITE,
        name='NOAA ISD Lite',
        parameters=[
            Parameters.TEMP,
            Parameters.PRCP,
            Parameters.WDIR
        ],
        handler='meteostat.provider.noaa.isd_lite'
    )
]