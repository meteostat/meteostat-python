"""
Meteorological Data Units

Convert a Pandas Series to any meteorological data unit

The code is licensed under the MIT license.
"""


def to_fahrenheit(value):
    """
    Convert Celsius to Fahrenheit
    """

    return round((value * 9 / 5) + 32, 1)


def to_kelvin(value):
    """
    Convert Celsius to Kelvin
    """

    return round(value + 273.15, 1)


def to_inches(value):
    """
    Convert millimeters to inches
    """

    return round(value / 25.4, 3)


def to_feet(value):
    """
    Convert meters to feet
    """

    return round(value / 0.3048, 1)


def to_meters_per_second(value):
    """
    Convert kilometers per hour to meters per second
    """

    return round(value / 3.6, 1)


def to_miles_per_hour(value):
    """
    Convert kilometers per hour to miles per hour
    """

    return round(value * 0.6214, 1)


def to_direction(value):
    """
    Convert degrees to wind direction
    """

    wdir = None

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


def to_condition(value):
    """
    Convert Meteostat condition code to descriptive string
    """

    if not value or value < 1 or value > 27:
        return None

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
