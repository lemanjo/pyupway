from __future__ import annotations
from dataclasses import dataclass
from ..enums import Variable
from datetime import datetime

@dataclass
class VariableValue:
    Id: int
    Name: str
    Enumerator: Variable
    Value: int | float | str | bool | None
    Unit: str | None
    EnumValue: str | None
    UpdatedAt: datetime | None
