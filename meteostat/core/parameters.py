"""
Parameter Service

The Parameter Service provides methods to manage and access
supported parameters for data requests.
"""

from typing import List, Optional

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

    def filter_parameters(
        self, granularity: Granularity, parameters: List[Parameter]
    ) -> List[Parameter]:
        """
        Raise exception if a requested parameter is not part of the schema
        """
        supported_parameters = list(
            map(
                lambda parameter: parameter.id,
                filter(
                    lambda parameter: parameter.granularity == granularity,
                    self.parameters,
                ),
            )
        )
        # Get difference between requested parameters and root schema
        diff = set(parameters).difference(supported_parameters)
        # Log warning
        if diff:
            logger.error(
                "Tried to request data for unsupported parameter(s): %s",
                ", ".join(diff),
            )
        # Return intersection
        return list(
            filter(
                lambda parameter: parameter in parameters,
                supported_parameters,
            )
        )


parameter_service = ParameterService(DEFAULT_PARAMETERS)
