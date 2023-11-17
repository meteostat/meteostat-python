from meteostat import Parameter
from meteostat.exceptions import ParameterException

def validate_parameters(supported: list[Parameter], requested: list[Parameter]) -> None:
    if not requested:
        return None
    diff = set(requested).difference(set(supported))
    if len(diff):
        raise ParameterException(f'Tried to request data for unsupported parameters: {", ".join([p.value for p in diff])}')