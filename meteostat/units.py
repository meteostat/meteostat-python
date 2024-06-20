"""
Meteorological Data Units

Convert a Pandas Series to any meteorological data unit

The code is licensed under the MIT license.
"""

from numpy import nan, isnan


def fahrenheit(value):
    """
    Convert Celsius to Fahrenheit
    """

    return round((value * 9 / 5) + 32, 1)


def kelvin(value):
    """
    Convert Celsius to Kelvin
    """

    return round(value + 273.15, 1)


def inches(value):
    """
    Convert millimeters to inches
    """

    return round(value / 25.4, 3)


def feet(value):
    """
    Convert meters to feet
    """

    return round(value / 0.3048, 1)


def ms(value):
    """
    Convert kilometers per hour to meters per second
    """

    return round(value / 3.6, 1)


def mph(value):
    """
    Convert kilometers per hour to miles per hour
    """

    return round(value * 0.6214, 1)


def direction(value):
    """
    Convert degrees to wind direction
    """

    wdir = nan

    if (337 <= value <= 360) or value <= 23:
        wdir = "N"
    if 24 <= value <= 68:
        wdir = "NE"
    if 69 <= value <= 113:
        wdir = "E"
    if 114 <= value <= 158:
        wdir = "SE"
    if 159 <= value <= 203:
        wdir = "S"
    if 204 <= value <= 248:
        wdir = "SW"
    if 249 <= value <= 293:
        wdir = "W"
    if 294 <= value <= 336:
        wdir = "NW"

    return wdir


def condition(value):
    """
    Convert Meteostat condition code to descriptive string
    """

    if isnan(value) or value < 1 or value > 27:
        return nan

    return [
        "Clear",
        "Fair",
        "Cloudy",
        "Overcast",
        "Fog",
        "Freezing Fog",
        "Light Rain",
        "Rain",
        "Heavy Rain",
        "Freezing Rain",
        "Heavy Freezing Rain",
        "Sleet",
        "Heavy Sleet",
        "Light Snowfall",
        "Snowfall",
        "Heavy Snowfall",
        "Rain Shower",
        "Heavy Rain Shower",
        "Sleet Shower",
        "Heavy Sleet Shower",
        "Snow Shower",
        "Heavy Snow Shower",
        "Lightning",
        "Hail",
        "Thunderstorm",
        "Heavy Thunderstorm",
        "Storm",
    ][int(value) - 1]


# Imperial units
imperial = {
    "temp": fahrenheit,
    "tavg": fahrenheit,
    "tmin": fahrenheit,
    "tmax": fahrenheit,
    "dwpt": fahrenheit,
    "prcp": inches,
    "snow": inches,
    "wspd": mph,
    "wpgt": mph,
    "distance": feet,
}

# Scientific units
scientific = {
    "temp": kelvin,
    "tavg": kelvin,
    "tmin": kelvin,
    "tmax": kelvin,
    "dwpt": kelvin,
    "wspd": ms,
    "wpgt": ms,
}
