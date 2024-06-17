from __future__ import annotations
from typing import List
from datetime import datetime

from .enums import DataService, Variable
from .config import MyUpwayConfig
from .models import VariableValue, VariableHistoryValue
from .services import MyUpwayService, MyUplinkService


class MyUpway:
    _config: MyUpwayConfig

    deviceId: str
    isOnline: bool

    def __init__(self, config: MyUpwayConfig) -> None:
        self._config = config

        if self._config.dataservice == DataService.MYUPWAY:
            self._service = MyUpwayService(self._config)
        else:
            self._service = MyUplinkService(self._config)

        self._service.login()

        self.deviceId = self._service.deviceId
        self.isOnline = self._service.isOnline

    def login(self):
        self._service.login()

    def get_current_values(self, variables: List[Variable] | None = None, force_login: bool = False) -> List[VariableValue]:
        """
        Returns current values for requested variables provided as list of VariableValue.
        If variables are not specified, function returns all variables.
        """

        return self._service.get_current_values(variables, force_login)

    def get_history_values(self, variable: Variable, startDate: datetime, stopDate: datetime, resolution: int = 1000, force_login: bool = False) -> List[VariableHistoryValue]:
        """
        MyUpway: Returns history values for selected variable from specified timerange.
        MyUplink: Not implemented. History data not available through new API.
        """

        return self._service.get_history_values(variable, startDate, stopDate, resolution, force_login)

    def logout(self):
        """
        MyUpway: Logs you out from the system.
        MyUplink: Not implemented as integration is token based API.
        """

        self._service.logout()
