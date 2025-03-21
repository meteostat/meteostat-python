from copy import copy
from typing import Callable, List

import pandas as pd

from meteostat.core.logger import logger
from meteostat.core.parameters import parameter_service
from meteostat.enumerations import Granularity, Parameter


class SchemaService:
    """
    Schema service
    """

    @staticmethod
    def _apply_validator(
        validator: Callable[[pd.Series], pd.Series], df: pd.DataFrame, col: str
    ) -> pd.Series:
        """
        Apply a validator
        """
        return validator(df[col])
    
    @staticmethod
    def purge(df: pd.DataFrame, granularity: Granularity) -> pd.DataFrame:
        """
        Remove DataFrame columns which are not a known parameter
        """
        parameters = parameter_service.get_parameters(granularity)
        columns = [
            parameter.id for parameter in parameters if parameter.id in df.columns
        ]
        return df[columns]
    
    @staticmethod
    def fill(df: pd.DataFrame, parameters: List[Parameter]) -> pd.DataFrame:
        """
        Add missing schema columns to DataFrame
        """
        for parameter_id in parameters:
            if parameter_id not in df:
                df[parameter_id] = None

        return df
    
    @staticmethod
    def format(df: pd.DataFrame, granularity: Granularity) -> pd.DataFrame:
        """
        Set data types and apply formatters to a DataFrame
        """
        temp = copy(df)

        for col in df.columns:
            parameter = parameter_service.get_parameter(col, granularity)

            if not parameter:
                logger.warning(
                    f"Column {col} is not a valid column name and won't be formatted"
                )

            if "int" in str(parameter.dtype).lower():
                temp[col] = pd.to_numeric(temp[col]).round(0)

            temp[col] = temp[col].astype(parameter.dtype, errors="ignore")

            for formatter in parameter.formatters:
                temp[col] = formatter(temp[col])

        return temp

    @classmethod
    def clean(
        cls, df: pd.DataFrame, granularity: Granularity, fill=None
    ) -> pd.DataFrame:
        """
        Remove invalid data from a DataFrame
        """
        temp = copy(df)

        for col in temp.columns:
            parameter = parameter_service.get_parameter(col, granularity)

            if not parameter:
                logger.warning(
                    f"Column {col} is not a valid column name and won't be cleaned"
                )

            for validator in parameter.validators:
                test = cls._apply_validator(validator, temp, col)
                temp.loc[~test, col] = fill

        return temp


schema_service = SchemaService()