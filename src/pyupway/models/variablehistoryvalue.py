from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class VariableHistoryValue:
    Value: int | float | str | bool | None
    Unit: str | None
    Date: datetime
