from enum import Enum
from typing import List

from backend.app.database import sqla_db as sqla


class ValueEnum(Enum):
    @classmethod
    def enum_values(cls) -> List:
        return [e.value for e in cls]

    @classmethod
    def sqla_values_enum(cls):
        return sqla.Enum(cls, values_callable=lambda x: cls.enum_values())
