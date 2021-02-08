import functools
from typing import List, Optional


def string_from_errors(errors: Optional[List[str]]) -> str:
    if not errors:
        return 'No errors'
    return functools.reduce(lambda x, y: x + f', {y}', errors, '')
