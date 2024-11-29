from datetime import date, timedelta
from meteostat.typing import ProviderDict
from meteostat.enumerations import Granularity, Parameter, Provider, Priority

PROVIDER_HOURLY = ProviderDict(
    id=Provider.HOURLY,
    granularity=Granularity.HOURLY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.SNWD,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.CLDC,
        Parameter.COCO,
    ],
    start=date(1931, 1, 1),
    module="meteostat.providers.data.hourly",
)

PROVIDER_DAILY = ProviderDict(
    id=Provider.DAILY,
    granularity=Granularity.DAILY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.SNWD,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.CLDC,
    ],
    start=date(1899, 1, 1),
    module="meteostat.providers.data.daily",
)

PROVIDER_DAILY_DERIVED = ProviderDict(
    id=Provider.DAILY_DERIVED,
    granularity=Granularity.DAILY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.PRCP,
        Parameter.SNOW,
        Parameter.WSPD,
        Parameter.WDIR,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.CLDC,
    ],
    start=date(1931, 1, 1),
    module="meteostat.providers.data.daily_derived",
)

PROVIDER_MONTHLY = ProviderDict(
    id=Provider.MONTHLY,
    granularity=Granularity.MONTHLY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.PRCP,
        Parameter.PRES,
        Parameter.TSUN,
    ],
    start=date(1899, 1, 1),
    module="meteostat.providers.data.monthly",
)

PROVIDER_MONTHLY_DERIVED = ProviderDict(
    id=Provider.MONTHLY_DERIVED,
    granularity=Granularity.MONTHLY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.PRCP,
        Parameter.PRES,
        Parameter.TSUN,
    ],
    start=date(1899, 1, 1),
    module="meteostat.providers.data.monthly_derived",
)

PROVIDER_DWD_HOURLY = ProviderDict(
    id=Provider.DWD_HOURLY,
    granularity=Granularity.HOURLY,
    priority=Priority.HIGHEST,
    countries=["DE"],
    parameters=[Parameter.TEMP, Parameter.PRCP, Parameter.WDIR],
    start=date(1939, 1, 1),
    module="meteostat.providers.dwd.hourly",
)

PROVIDER_DWD_POI = ProviderDict(
    id=Provider.DWD_POI,
    granularity=Granularity.HOURLY,
    priority=Priority.HIGH,
    parameters=[
        Parameter.CLDC,
        Parameter.TEMP,
        Parameter.VSBY,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRCP,
        Parameter.RHUM,
        Parameter.WDIR,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.COCO,
        Parameter.SNWD,
    ],
    start=date.today() - timedelta(days=1),
    module="meteostat.providers.dwd.poi",
)

PROVIDER_DWD_MOSMIX = ProviderDict(
    id=Provider.DWD_MOSMIX,
    granularity=Granularity.HOURLY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.CLDC,
        Parameter.COCO,
    ],
    start=date.today(),
    module="meteostat.providers.dwd.mosmix",
)

PROVIDER_DWD_DAILY = ProviderDict(
    id=Provider.DWD_DAILY,
    granularity=Granularity.DAILY,
    priority=Priority.HIGHEST,
    countries=["DE"],
    parameters=[],
    start=date(1781, 1, 1),
    module="meteostat.providers.dwd.daily",
)

PROVIDER_DWD_MONTHLY = ProviderDict(
    id=Provider.DWD_MONTHLY,
    granularity=Granularity.MONTHLY,
    priority=Priority.HIGHEST,
    countries=["DE"],
    parameters=[Parameter.TAVG, Parameter.TMIN, Parameter.TMAX, Parameter.PRCP],
    start=date(1851, 1, 1),
    module="meteostat.providers.dwd.monthly",
)

PROVIDER_ECCC_HOURLY = ProviderDict(
    id=Provider.ECCC_HOURLY,
    granularity=Granularity.HOURLY,
    priority=Priority.HIGHEST,
    countries=["CA"],
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.VSBY,
    ],
    start=date(1939, 1, 1),
    module="meteostat.providers.eccc.hourly",
)

PROVIDER_ECCC_DAILY = ProviderDict(
    id=Provider.ECCC_DAILY,
    granularity=Granularity.DAILY,
    priority=Priority.HIGHEST,
    countries=["CA"],
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.PRCP,
        Parameter.SNOW,
        Parameter.SNWD,
        Parameter.WPGT,
    ],
    start=date(1939, 1, 1),
    module="meteostat.providers.eccc.daily",
)

PROVIDER_ECCC_MONTHLY = ProviderDict(
    id=Provider.ECCC_MONTHLY,
    granularity=Granularity.MONTHLY,
    priority=Priority.HIGHEST,
    countries=["CA"],
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.PRCP,
        Parameter.PDAY,
        Parameter.SNOW,
    ],
    start=date(1939, 1, 1),
    module="meteostat.providers.eccc.monthly",
)

PROVIDER_ISD_LITE = ProviderDict(
    id=Provider.ISD_LITE,
    granularity=Granularity.HOURLY,
    priority=Priority.HIGH,
    parameters=[Parameter.TEMP, Parameter.PRCP, Parameter.WDIR],
    start=date(1931, 1, 1),
    module="meteostat.providers.noaa.isd_lite",
)

PROVIDER_GHCND = ProviderDict(
    id=Provider.GHCND,
    granularity=Granularity.DAILY,
    priority=Priority.HIGH,
    parameters=[
        Parameter.TAVG,
        Parameter.TMIN,
        Parameter.TMAX,
        Parameter.PRCP,
        Parameter.SNOW,
        Parameter.WSPD,
        Parameter.WDIR,
        Parameter.WPGT,
        Parameter.TSUN,
        Parameter.CLDC,
    ],
    start=date(1931, 1, 1),
    module="meteostat.providers.noaa.ghcnd",
)

PROVIDER_METAR = ProviderDict(
    id=Provider.METAR,
    granularity=Granularity.HOURLY,
    priority=Priority.LOW,
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.PRES,
        Parameter.COCO,
    ],
    start=date.today() - timedelta(days=1),
    module="meteostat.providers.noaa.metar",
)

PROVIDER_METNO_FORECAST = ProviderDict(
    id=Provider.METNO_FORECAST,
    granularity=Granularity.HOURLY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.CLDC,
        Parameter.COCO,
    ],
    start=date.today(),
    module="meteostat.providers.metno.forecast",
)


# Archived providers

PROVIDER_SYNOP = ProviderDict(
    id="synop",
    granularity=Granularity.HOURLY,
    priority=Priority.MEDIUM,
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.SNOW,
        Parameter.SNWD,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.SGHI,
        Parameter.SDNI,
        Parameter.SDHI,
        Parameter.CLDC,
        Parameter.VSBY,
        Parameter.COCO,
    ],
    start=date(2015, 8, 7),
)

PROVIDER_MODEL = ProviderDict(
    id="model",
    granularity=Granularity.HOURLY,
    priority=Priority.LOWEST,
    parameters=[
        Parameter.TEMP,
        Parameter.RHUM,
        Parameter.PRCP,
        Parameter.WDIR,
        Parameter.WSPD,
        Parameter.WPGT,
        Parameter.PRES,
        Parameter.TSUN,
        Parameter.CLDC,
        Parameter.COCO,
    ],
    start=date(2015, 8, 7),
)


# All providers

ALL_PROVIDERS = [
    PROVIDER_HOURLY,
    PROVIDER_DAILY,
    PROVIDER_DAILY_DERIVED,
    PROVIDER_MONTHLY,
    PROVIDER_MONTHLY_DERIVED,
    PROVIDER_DWD_HOURLY,
    PROVIDER_DWD_POI,
    PROVIDER_DWD_MOSMIX,
    PROVIDER_DWD_DAILY,
    PROVIDER_DWD_MONTHLY,
    PROVIDER_ECCC_HOURLY,
    PROVIDER_ECCC_DAILY,
    PROVIDER_ECCC_MONTHLY,
    PROVIDER_ISD_LITE,
    PROVIDER_GHCND,
    PROVIDER_METAR,
    PROVIDER_METNO_FORECAST,
    PROVIDER_SYNOP,
    PROVIDER_MODEL,
]
