from meteostat.units import (
    to_fahrenheit,
    to_kelvin,
    to_inches,
    to_feet,
    to_meters_per_second,
    to_miles_per_hour,
    to_direction,
    to_condition,
)


def test_to_fahrenheit():
    assert to_fahrenheit(0) == 32.0
    assert to_fahrenheit(100) == 212.0
    assert to_fahrenheit(-40) == -40.0
    assert to_fahrenheit(37) == 98.6


def test_to_kelvin():
    assert to_kelvin(0) == 273.1
    assert to_kelvin(100) == 373.1
    assert to_kelvin(-273.15) == 0.0
    assert to_kelvin(25) == 298.1


def test_to_inches():
    assert to_inches(25.4) == 1.0
    assert to_inches(50.8) == 2.0
    assert to_inches(0) == 0.0
    assert to_inches(12.7) == 0.5


def test_to_feet():
    assert to_feet(1) == 3.3
    assert to_feet(0) == 0.0
    assert to_feet(0.3048) == 1.0
    assert to_feet(10) == 32.8


def test_to_meters_per_second():
    assert to_meters_per_second(36) == 10.0
    assert to_meters_per_second(0) == 0.0
    assert to_meters_per_second(3.6) == 1.0
    assert to_meters_per_second(72) == 20.0


def test_to_miles_per_hour():
    assert to_miles_per_hour(100) == 62.1
    assert to_miles_per_hour(0) == 0.0
    assert to_miles_per_hour(1.60934) == 1.0
    assert to_miles_per_hour(50) == 31.1


def test_to_direction():
    assert to_direction(0) == "N"
    assert to_direction(45) == "NE"
    assert to_direction(90) == "E"
    assert to_direction(135) == "SE"
    assert to_direction(180) == "S"
    assert to_direction(225) == "SW"
    assert to_direction(270) == "W"
    assert to_direction(315) == "NW"
    assert to_direction(360) == "N"
    assert to_direction(23) == "N"
    assert to_direction(24) == "NE"
    assert to_direction(68) == "NE"
    assert to_direction(69) == "E"
    assert to_direction(113) == "E"
    assert to_direction(114) == "SE"
    assert to_direction(158) == "SE"
    assert to_direction(159) == "S"
    assert to_direction(203) == "S"
    assert to_direction(204) == "SW"
    assert to_direction(248) == "SW"
    assert to_direction(249) == "W"
    assert to_direction(293) == "W"
    assert to_direction(294) == "NW"
    assert to_direction(336) == "NW"
    assert to_direction(337) == "N"
    assert to_direction(22) == "N"
    assert to_direction(69) == "E"
    assert to_direction(180) == "S"
    assert to_direction(248) == "SW"
    assert to_direction(337) == "N"


def test_to_condition():
    assert to_condition(1) == "Clear"
    assert to_condition(2) == "Fair"
    assert to_condition(3) == "Cloudy"
    assert to_condition(27) == "Storm"
    assert to_condition(0) is None
    assert to_condition(28) is None
    assert to_condition(-1) is None
    assert to_condition(None) is None
    assert to_condition(5) == "Fog"
