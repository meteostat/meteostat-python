from pulire import Schema, Column, validators, formatters

from meteostat.enumerations import Parameter

HOURLY_SCHEMA = Schema(
    [
        Column(
            Parameter.TEMP,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.DWPT,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.RHUM,
            "UInt8",
            [validators.minimum(0), validators.maximum(100)],
        ),
        Column(
            Parameter.PRCP,
            "Float32",
            [validators.minimum(0), validators.maximum(350), formatters.decimals(1)],
        ),
        Column(
            Parameter.SNOW,
            "UInt8",
            [validators.minimum(0), validators.maximum(50)],
        ),
        Column(
            Parameter.SNWD,
            "UInt16",
            [validators.minimum(0), validators.maximum(1200)],
        ),
        Column(
            Parameter.WDIR,
            "UInt16",
            [validators.minimum(0), validators.maximum(360)],
        ),
        Column(
            Parameter.WSPD,
            "Float32",
            [validators.minimum(0), validators.maximum(250), formatters.decimals(1)],
        ),
        Column(
            Parameter.WPGT,
            "Float32",
            [validators.minimum(0), validators.maximum(500), formatters.decimals(1)],
        ),
        Column(
            Parameter.PRES,
            "Float32",
            [validators.minimum(850), validators.maximum(1090), formatters.decimals(1)],
        ),
        Column(
            Parameter.TSUN,
            "UInt8",
            [validators.minimum(0), validators.maximum(60)],
        ),
        Column(
            Parameter.CLDC,
            "UInt8",
            [validators.minimum(0), validators.maximum(8)],
        ),
        Column(
            Parameter.VSBY,
            "UInt16",
            [validators.minimum(0)],
        ),
        Column(
            Parameter.COCO,
            "UInt8",
            [validators.minimum(0), validators.maximum(27)],
        ),
    ]
)

DAILY_SCHEMA = Schema(
    [
        Column(
            Parameter.TAVG,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.TMIN,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.TMAX,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.DWPT,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.RHUM,
            "Int64",
            [validators.minimum(0), validators.maximum(100)],
        ),
        Column(
            Parameter.PRCP,
            "Float32",
            [validators.minimum(0), validators.maximum(2000), formatters.decimals(1)],
        ),
        Column(
            Parameter.SNOW,
            "Int64",
            [validators.minimum(0), validators.maximum(50), formatters.decimals(1)],
        ),
        Column(
            Parameter.SNWD,
            "UInt8",
            [validators.minimum(0), validators.maximum(200)],
        ),
        Column(
            Parameter.WSPD,
            "Float32",
            [validators.minimum(0), validators.maximum(150), formatters.decimals(1)],
        ),
        Column(
            Parameter.WPGT,
            "Float32",
            [validators.minimum(0), validators.maximum(500), formatters.decimals(1)],
        ),
        Column(
            Parameter.PRES,
            "Float32",
            [validators.minimum(850), validators.maximum(1090), formatters.decimals(1)],
        ),
        Column(
            Parameter.TSUN,
            "UInt16",
            [validators.minimum(0), validators.maximum(1440)],
        ),
        Column(
            Parameter.CLDC,
            "UInt8",
            [validators.minimum(0), validators.maximum(8)],
        ),
        Column(
            Parameter.VSBY,
            "UInt16",
            [validators.minimum(0)],
        ),
    ]
)

MONTHLY_SCHEMA = Schema(
    [
        Column(
            Parameter.TAVG,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.TAMN,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.TAMX,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.TMIN,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.TMAX,
            "Float32",
            [validators.minimum(-100), validators.maximum(65), formatters.decimals(1)],
        ),
        Column(
            Parameter.PRCP,
            "Float32",
            [validators.minimum(0), validators.maximum(10000), formatters.decimals(1)],
        ),
        Column(
            Parameter.PRES,
            "Float32",
            [validators.minimum(850), validators.maximum(1090), formatters.decimals(1)],
        ),
        Column(
            Parameter.TSUN,
            "UInt16",
            [validators.minimum(0), validators.maximum(44640)],
        ),
    ]
)

NORMALS_SCHEMA = MONTHLY_SCHEMA
