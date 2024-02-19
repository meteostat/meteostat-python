from typing import List
from meteostat.typing import ParameterDict
from meteostat.enumerations import Granularity, Parameter
from meteostat.utils.aggregations import degree_mean


PARAMETERS: List[ParameterDict] = [
    {
        "id": Parameter.TEMP,
        "name": "Air Temperature",
        "dtype": "Float64",
        "aggregation": "mean",
        "granularities": [{"granularity": Granularity.HOURLY, "default": True}],
    },
    {
        "id": Parameter.TAVG,
        "name": "Average Air Temperature",
        "dtype": "Float64",
        "aggregation": "mean",
        "granularities": [{"granularity": Granularity.DAILY, "default": True}],
    },
    {
        "id": Parameter.TMIN,
        "name": "Minimum Air Temperature",
        "dtype": "Float64",
        "aggregation": "min",
        "granularities": [{"granularity": Granularity.DAILY, "default": True}],
    },
    {
        "id": Parameter.TMAX,
        "name": "Maximum Air Temperature",
        "dtype": "Float64",
        "aggregation": "max",
        "granularities": [{"granularity": Granularity.DAILY, "default": True}],
    },
    {
        "id": Parameter.RHUM,
        "name": "Relative Humidity",
        "dtype": "Int64",
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY},
        ],
    },
    {
        "id": Parameter.DWPT,
        "name": "Dew Point Temperature",
        "dtype": "Float64",
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY},
            {"granularity": Granularity.DAILY},
        ],
    },
    {
        "id": Parameter.PRCP,
        "name": "Precipitation",
        "dtype": "Float64",
        "aggregation": "sum",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.SNOW,
        "name": "Snowfall",
        "dtype": "Int64",
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
        "dtype": "Int64",
        "aggregation": "max",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.WDIR,
        "name": "Wind Direction",
        "dtype": "Int64",
        "aggregation": degree_mean,
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.WSPD,
        "name": "Wind Speed",
        "dtype": "Float64",
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.WPGT,
        "name": "Wind Peak Gust",
        "dtype": "Float64",
        "aggregation": "max",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.PRES,
        "name": "Sea-Level Air Pressure",
        "dtype": "Float64",
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.TSUN,
        "name": "Sunshine Duration",
        "dtype": "Int64",
        "aggregation": "sum",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.CLDC,
        "name": "Cloud Cover",
        "dtype": "Int64",
        "aggregation": "mean",
        "granularities": [
            {"granularity": Granularity.HOURLY, "default": True},
            {"granularity": Granularity.DAILY, "default": True},
        ],
    },
    {
        "id": Parameter.VSBY,
        "name": "Visibility",
        "dtype": "Int64",
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
        "dtype": "Int64",
        "granularities": [{"granularity": Granularity.HOURLY, "default": True}],
    },
]
