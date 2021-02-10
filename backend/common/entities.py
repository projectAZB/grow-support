from typing import Optional

from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:
    id: Optional[int]
