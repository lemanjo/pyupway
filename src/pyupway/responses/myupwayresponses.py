from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Any

from ..models import ValueModel

@dataclass
class ValueResponseModel:
    IsOffline: bool
    OnlineImage: str
    Date: datetime
    FuzzyDate: str
    Values: List[ValueModel]

@dataclass
class HistoryResponseModel:
    label: str
    data: List[List[Any]]
    color: str
    variableid: int
    unit: str
    isfullzoom: bool
    reloadoverview: bool
    yaxis: int
    NumberOfDecimals: int