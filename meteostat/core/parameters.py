from typing import List
from meteostat.typing import ParameterDict
from meteostat.enumerations import Granularity, Parameter
from meteostat.utils.aggregations import degree_mean


PARAMETERS: List[ParameterDict] = [
    {
        "id": Parameter.TEMP,
        "name": "Air Temperature",
        "dtype": float,
        "aggregation": "mean",
        "granularities": [{"granularity": Granularity.HOURLY, "default": True}],
    },
    {
        "id": Parameter.TAVG,
        "name": "Average Air Temperature",
        "dtype": float,
        "aggregation": "mean",
        "granularities": [{"granularity": Granularity.DAILY, "default": True}],
    },
    {
        "id": Parameter.TMIN,
        "name": "Minimum Air Temperature",
        "dtype": float,
        "aggregation": "min",
        "granularities": [{"granularity": Granularity.DAILY, "default": True}],
    },
    {
        "id": Parameter.TMAX,
        "name": "Maximum Air Temperature",
        "dtype": float,
        "aggregation": "max",
        "granularities": [{"granularity": Granularity.DAILY, "default": True}],
    },
    {
        "id": Parameter.RHUM,
        "name": "Relative Humidity",
        "dtype": int,
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY},
        ],
    },
    {
        "id": Parameter.DWPT,
        "name": "Dew Point Temperature",
        "dtype": float,
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY},
            {"granularity": Granularity.DAILY},
        ],
    },
    {
        "id": Parameter.PRCP,
        "name": "Precipitation",
        "dtype": float,
        "aggregation": "sum",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.SNOW,
        "name": "Snowfall",
        "dtype": int,
        "aggregation": "sum",
        "granularities": [
            {
                "granularity": Granularity.HOURLY,
            },
            {
                "granularity": Granularity.DAILY,
            },
        ],
    },
    {
        "id": Parameter.SNWD,
        "name": "Snow Depth",
        "dtype": int,
        "aggregation": "max",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.WDIR,
        "name": "Wind Direction",
        "dtype": int,
        "aggregation": degree_mean,
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.WSPD,
        "name": "Wind Speed",
        "dtype": float,
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.WPGT,
        "name": "Wind Peak Gust",
        "dtype": float,
        "aggregation": "max",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.PRES,
        "name": "Sea-Level Air Pressure",
        "dtype": float,
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.TSUN,
        "name": "Sunshine Duration",
        "dtype": int,
        "aggregation": "sum",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.CLDC,
        "name": "Cloud Cover",
        "dtype": int,
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.VSBY,
        "name": "Visibility",
        "dtype": int,
        "aggregation": "mean",
        "granularities": [
            {
                "granularity": Granularity.HOURLY,
            },
            {
                "granularity": Granularity.DAILY,
            },
        ],
    },
    {
        "id": Parameter.COCO,
        "name": "Weather Condition Code",
        "dtype": int,
        "granularities": [{"granularity": Granularity.HOURLY, "default": True}],
    },
]
