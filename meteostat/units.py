"""
Meteorological Data Units

Convert a Pandas Series to any meteorological data unit

The code is licensed under the MIT license.
"""

from math import nan, isnan

# Convert Celsius to Fahrenheit
def fahrenheit(value):

    return round((value * 9/5) + 32, 1)

# Convert Celsius to Kelvin
def kelvin(value):

    return round(value + 273.15, 1)

# Convert millimeters to inches
def inches(value):

    return round(value / 25.4, 1)

# Convert meters to feet
def feet(value):

    return round(value / 0.3048, 1)

# Convert kilometers per hour to meters per second
def ms(value):

    return round(value / 3.6, 1)

# Convert kilometers per hour to miles per hour
def mph(value):

    return round(value * 0.6214, 1)

# Convert degrees to wind direction
def direction(value):

    if (value >= 337 and value <= 360) or value <= 23:
        return 'N'
    elif value >= 24 and value <= 68:
        return 'NE'
    elif value >= 69 and value <= 113:
        return 'E'
    elif value >= 114 and value <= 158:
        return 'SE'
    elif value >= 159 and value <= 203:
        return 'S'
    elif value >= 204 and value <= 248:
        return 'SW'
    elif value >= 249 and value <= 293:
        return 'W'
    elif value >= 294 and value <= 336:
        return 'NW'
    else:
        return nan


# Convert Meteostat condition code to descriptive string
def condition(value):

    if isnan(value) or value < 1 or value > 27:
        return nan
    else:
        return [
            'Clear',
            'Fair',
            'Cloudy',
            'Overcast',
            'Fog',
            'Freezing Fog',
            'Light Rain',
            'Rain',
            'Heavy Rain',
            'Freezing Rain',
            'Heavy Freezing Rain',
            'Sleet',
            'Heavy Sleet',
            'Light Snowfall',
            'Snowfall',
            'Heavy Snowfall',
            'Rain Shower',
            'Heavy Rain Shower',
            'Sleet Shower',
            'Heavy Sleet Shower',
            'Snow Shower',
            'Heavy Snow Shower',
            'Lightning',
            'Hail',
            'Thunderstorm',
            'Heavy Thunderstorm',
            'Storm',
        ][int(value) - 1]
