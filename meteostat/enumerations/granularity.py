""" granularity of data types enumeration """
from enum import Enum


class Granularity(Enum):
    """ granularity of data types enumeration """

    HOURLY = 'hourly'
    DAILY = 'daily'
    MONTHLY = 'monthly'
    NORMALS = 'normals'