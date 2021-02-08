from typing import Optional

from dataclasses import dataclass


@dataclass(frozen=True)
class Base:
    id: Optional[int]
