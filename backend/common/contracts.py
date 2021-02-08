from abc import ABC
from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class BaseRequest(ABC):
    pass


@dataclass(frozen=True)
class PayloadData(ABC):
    pass


@dataclass(frozen=True)
class BaseResponse(ABC):
    success: bool
    errors: Optional[List[str]] = None
    data: Optional[PayloadData] = None
