"""
Inventory Module

Provides classes for working with weather station data inventories.
"""

from datetime import date, datetime

import pandas as pd

from meteostat.enumerations import Parameter


class Inventory:
    """
    A weather station's data inventory
    """

    df: pd.DataFrame | None = None

    def __init__(self, df: pd.DataFrame | None = None):
        if df is not None and not df.empty:
            self.df = df

    @property
    def start(self) -> date | None:
        """
        Get the earliest start date from the inventory
        """
        return datetime.strptime(self.df["start"].min(), "%Y-%m-%d").date() if self.df is not None else None

    @property
    def end(self) -> date | None:
        """
        Get the latest end date from the inventory
        """
        return datetime.strptime(self.df["end"].max(), "%Y-%m-%d").date() if self.df is not None else None

    @property
    def parameters(self) -> list[Parameter] | None:
        """
        Get the list of available parameters from the inventory
        """
        if self.df is None:
            return []

        return [Parameter[parameter.upper()] for parameter in self.df.index.get_level_values("parameter").unique()]
