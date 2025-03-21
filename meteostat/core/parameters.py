from copy import copy
from inspect import isfunction
from typing import Callable, List, Optional

import pandas as pd

from meteostat.core.logger import logger
from meteostat.enumerations import Granularity, Parameter
from meteostat.parameters import DEFAULT_PARAMETERS
from meteostat.typing import ParameterSpec


class ParameterService:
    """
    Parameter Service
    """

    _parameters: List[ParameterSpec]

    @staticmethod
    def _has_duplicates(parameter_specs: List[ParameterSpec]) -> bool:
        """
        Check if parameter list contains duplicates
        """
        seen = set()
        for spec in parameter_specs:
            key = (spec.id, spec.granularity)
            if key in seen:
                return True  # Duplicate found
            seen.add(key)
        return False  # No duplicates found

    def _parameter_exists(self, parameter: ParameterSpec) -> bool:
        """
        Check if a parameter already exists
        """
        key = (parameter.id, parameter.granularity)
        return any((spec.id, spec.granularity) == key for spec in self.parameters)

    @staticmethod
    def _apply_validator(
        validator: Callable[[pd.Series], pd.Series], df: pd.DataFrame, col: str
    ) -> pd.Series:
        """
        Apply a validator
        """
        func = validator() if isfunction(validator) else validator
        return func(df[col])

    def __init__(self, parameters: List[ParameterSpec]) -> None:
        if self._has_duplicates(parameters):
            raise ValueError("List of parameters contains duplicates")

        self._parameters = parameters

    @property
    def parameters(self) -> List[ParameterSpec]:
        """
        Get supported parameters
        """
        return self._parameters

    def register(self, parameter: ParameterSpec) -> None:
        """
        Register a parameter
        """
        if self._parameter_exists(parameter):
            raise ValueError("The parameter already exists")

        self._parameters.append(parameter)

    def get_parameters(self, granularity: Granularity) -> List[ParameterSpec]:
        """
        Get list of parameters by granularity
        """
        return [spec for spec in self.parameters if spec.granularity == granularity]

    def get_parameter(
        self, parameter_id: Parameter, granularity: Granularity
    ) -> Optional[ParameterSpec]:
        """
        Get parameter by ID and granularity
        """
        return next(
            (
                parameter
                for parameter in self.parameters
                if parameter.id == parameter_id and parameter.granularity == granularity
            ),
            None,
        )

    def purge_df(self, df: pd.DataFrame, granularity: Granularity) -> pd.DataFrame:
        """
        Remove DataFrame columns which are not a known parameter
        """
        parameters = self.get_parameters(granularity)
        columns = [
            parameter.id for parameter in parameters if parameter.id in df.columns
        ]
        return df[columns]

    @staticmethod
    def fill_df(df: pd.DataFrame, parameters: List[Parameter]) -> pd.DataFrame:
        """
        Add missing schema columns to DataFrame
        """
        for parameter_id in parameters:
            if parameter_id not in df:
                df[parameter_id] = None

        return df

    def format_df(self, df: pd.DataFrame, granularity: Granularity) -> pd.DataFrame:
        """
        Set data types and apply formatters to a DataFrame
        """
        temp = copy(df)

        for col in df.columns:
            parameter = self.get_parameter(col, granularity)

            if not parameter:
                logger.warning(
                    f"Column {col} is not a valid column name and won't be formatted"
                )

            if "int" in str(parameter.dtype).lower():
                temp[col] = pd.to_numeric(temp[col]).round(0)

            temp[col] = temp[col].astype(parameter.dtype, errors="ignore")

            for formatter in parameter.formatters:
                func = formatter() if isfunction(formatter) else formatter
                temp[col] = func(temp[col])

        return temp

    def clean_df(
        self, df: pd.DataFrame, granularity: Granularity, fill=None
    ) -> pd.DataFrame:
        """
        Remove invalid data from a DataFrame
        """
        temp = copy(df)

        for col in temp.columns:
            parameter = self.get_parameter(col, granularity)

            if not parameter:
                logger.warning(
                    f"Column {col} is not a valid column name and won't be cleaned"
                )

            for validator in parameter.validators:
                test = self._apply_validator(validator, temp, col)
                temp.loc[~test, col] = fill

        return temp


parameter_service = ParameterService(DEFAULT_PARAMETERS)
