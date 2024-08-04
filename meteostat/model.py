from datetime import date
from meteostat.typing import ProviderDict
from meteostat.enumerations import Granularity, Parameter, Provider, Priority

PARAMETER_DTYPES = {
    Parameter.TEMP: "Float64",
    Parameter.TAVG: "Float64",
    Parameter.TMIN: "Float64",
    Parameter.TMAX: "Float64",
    Parameter.RHUM: "Int64",
    Parameter.DWPT: "Float64",
    Parameter.PRCP: "Float64",
    Parameter.SNOW: "Int64",
    Parameter.SNWD: "Int64",
    Parameter.WDIR: "Int64",
    Parameter.WSPD: "Float64",
    Parameter.WPGT: "Float64",
    Parameter.PRES: "Float64",
    Parameter.TSUN: "Int64",
    Parameter.CLDC: "Int64",
    Parameter.VSBY: "Int64",
    Parameter.COCO: "Int64",
}

PARAMETER_DESCRIPTIONS = {
    Parameter.TEMP: "Air Temperature",
    Parameter.TAVG: "Average Air Temperature",
    Parameter.TMIN: "Minimum Air Temperature",
    Parameter.TMAX: "Maximum Air Temperature",
    Parameter.RHUM: "Relative Humidity",
    Parameter.DWPT: "Dew Point Temperature",
    Parameter.PRCP: "Precipitation",
    Parameter.SNOW: "Snowfall",
    Parameter.SNWD: "Snow Depth",
    Parameter.WDIR: "Wind Direction",
    Parameter.WSPD: "Wind Speed",
    Parameter.WPGT: "Peak Wind Gust",
    Parameter.PRES: "Sea-Level Air Pressure",
    Parameter.TSUN: "Sunshine Duration",
    Parameter.CLDC: "Cloud Cover",
    Parameter.VSBY: "Visibility",
    Parameter.COCO: "Weather Condition Code",
}

PROVIDER_BULK_HOURLY = ProviderDict(
    id=Provider.BULK_HOURLY,
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
    module="meteostat.providers.bulk.hourly",
)

PROVIDER_BULK_DAILY = ProviderDict(
    id=Provider.BULK_DAILY,
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
    module="meteostat.providers.bulk.daily",
)

PROVIDER_BULK_DAILY_DERIVED = ProviderDict(
    id=Provider.BULK_DAILY_DERIVED,
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
    module="meteostat.providers.bulk.daily_derived",
)

PROVIDER_BULK_MONTHLY = ProviderDict(
    id=Provider.BULK_MONTHLY,
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
    module="meteostat.providers.bulk.monthly",
)

PROVIDER_BULK_MONTHLY_DERIVED = ProviderDict(
    id=Provider.BULK_MONTHLY_DERIVED,
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
    module="meteostat.providers.bulk.monthly_derived",
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

PROVIDER_SYNOP = ProviderDict(
    id=Provider.SYNOP,
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
    module="meteostat.providers.meteostat.synop",
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
    start=date(2015, 8, 7),
    module="meteostat.providers.meteostat.metar",
)

PROVIDER_MODEL = ProviderDict(
    id=Provider.MODEL,
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
    module="meteostat.providers.meteostat.model",
)
