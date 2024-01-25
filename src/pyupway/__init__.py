from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Any
from datetime import datetime

import requests
import re


class MyUpwayConfig:
    username: str
    password: str
    heatpump_id: int

    def __init__(self, username: str, password: str, heatpump_id: int) -> None:
        self.username = username
        self.password = password
        self.heatpump_id = heatpump_id


@dataclass
class VariableValue:
    Id: int
    Name: str
    Enumerator: Variable
    Value: int | float | str | bool | None
    Unit: str | None


@dataclass
class VariableHistoryValue:
    Value: int | float | str | bool | None
    Unit: str | None
    Date: datetime


@dataclass
class ValueModel:
    VariableId: int
    CurrentValue: str


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


TIME_REPRESENTATION_FORMATS = [
    "%m/%d/%Y %H:%M:%S",
    "%Y. %m. %d. %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H.%M.%S"
]


class Variable(Enum):
    """
    Provides Variable name - Variable ID mapping as enum
    """

    AVG_OUTDOOR_TEMP = 40067
    HOT_WATER_CHARGING = 40014                  # TehoWatti AIR
    HOT_WATER_TOP = 40013                       # TehoWatti AIR
    INDOOR_UNIT_OUTDOOR_TEMP = 40004
    CURRENT_BE1 = 40083
    CURRENT_BE2 = 40081
    CURRENT_BE3 = 40079
    DEGREE_MINUTES = 43005
    EXTERNAL_ADJUSTMENT = 43161
    FLOOR_DRYING_FUNCTION = 47276
    CALCULATED_FLOW_TEMP = 43009
    EXTERNAL_FLOW_TEMP = 40071
    EXTERNAL_RETURN_TEMP = 40152
    HEAT_MEDIUM_FLOW = 40008                    # TehoWatti AIR
    HEAT_RETURN_TEMP = 40012                    # TehoWatti AIR
    ROOM_TEMPERATURE = 40033
    ADDITION_BLOCKED = 10033
    ADDITION_MAX_STEP = 47613
    ADDITION_STATUS = 43091
    ADDITION_FUSE_SIZE = 47214
    ADDITION_TIME_FACTOR = 43081                # TehoWatti AIR
    ADDITION_ELECTRICAL_ADDITION_POWER = 43084  # TehoWatti AIR
    ADDITION_SET_MAX_ELECTRICAL_ADD = 47212     # TehoWatti AIR
    ADDITION_TEMPERATURE = 40121                # TehoWatti AIR
    ENERGY_COOLING_COMPRESSOR_ONLY = 44302      # TehoWatti AIR
    ENERGY_HEATING_COMPRESSOR_ONLY = 44308      # TehoWatti AIR
    ENERGY_HEATING_INT_ADD_INCL = 44300         # TehoWatti AIR
    ENERGY_HOTWATER_COMPRESSOR_ONLY = 44306     # TehoWatti AIR
    ENERGY_HW_INCL_INT_ADD = 44298              # TehoWatti AIR
    ENERGY_POOL_COMPRESSOR_ONLY = 44304         # TehoWatti AIR
    ENERGY_FLOW = 40072                         # TehoWatti AIR
    AUX1 = 47411
    AUX2 = 47410
    AUX3 = 47409
    AUX4 = 47408
    AUX5 = 47407
    AUX6 = 48366
    X7 = 47412
    COUNTRY = 48745
    DEFROSTING = 44703
    CHARGE_PUMP_SPEED = 44396
    OUTDOOR_UNIT_OUTDOOR_TEMP = 44362
    COMPRESSOR_BLOCKED = 10014
    COMPRESSOR_STARTS = 44069
    COMPRESSOR_PROTECTION_MODE = 44702
    CONDENSER_OUT = 44058
    EVAPORATOR = 44363
    HOT_GAS = 44059
    LIQUID_LINE = 44060
    RETURN_TEMP = 44055
    SUCTION_GAS = 44061
    HIGH_PRESSURE_SENSOR = 44699
    LOW_PRESSURE_SENSOR = 44700
    COMPRESSOR_OPERATING_TIME = 44071
    COMPRESSOR_OPERATING_TIME_HOT_WATER = 44073
    COMPRESSOR_RUN_TIME_COOLING = 40737
    CURRENT_COMPRESSOR_FREQUENCY = 44701
    REQUESTED_COMPRESSOR_FREQUENCY = 40782
    VERSION = 44014
    SMART_PRICE_STATUS = 44908          # Metro-air 330
    SMART_PRICE_VALUE = 10069             # Metro-air 330
    SMART_PRICE_FACTOR = 44896          # Metro-air 330

class LoginError(Exception):
    pass


class NotLoggedIn(Exception):
    pass


class ResponseError(Exception):
    pass


class MyUpway:
    _BASE_URL = 'https://www.myupway.com'

    _config: MyUpwayConfig
    _session: requests.Session

    isOnline: bool

    def __init__(self, config: MyUpwayConfig) -> None:
        self._config = config
        self._session = requests.Session()
        self._login()

    def _login(self) -> None:

        url = self._BASE_URL + '/LogIn'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'returnUrl': '',
            'Email': self._config.username,
            'Password': self._config.password
        }

        response = self._session.post(url, headers=headers, data=data)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Request failed with status code {response.status_code}")

        if not '.ASPXAUTH' in self._session.cookies:
            raise LoginError("Login failed.")

    def get_current_values(self, variables: List[Variable] | None = None, force_login: bool = False) -> List[VariableValue]:
        """
        Returns current values for requested variables provided as list of VariableValue.
        If variables are not specified, function returns all variables.
        """

        url = self._BASE_URL + '/PrivateAPI/Values'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = [
            ('hpid', self._config.heatpump_id)
        ]

        if not variables:
            variables = list(Variable)

        for variable in variables:
            data.append(('variables', variable.value))  # type: ignore

        if not '.ASPXAUTH' in self._session.cookies and force_login:
            self._login()

        if not '.ASPXAUTH' in self._session.cookies:
            raise NotLoggedIn(
                "Session is not currenly logged in. Use force_login = True if you want to force relogin.")

        response = self._session.post(url, headers=headers, data=data)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Request failed with status code {response.status_code}, data: {response}")

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise ResponseError(
                f"Cannot parse response data. Data: {response.content}")

        for timeformat in TIME_REPRESENTATION_FORMATS:
            try:
                response_data['Date'] = datetime.strptime(
                    response_data['Date'], timeformat)

            except ValueError:
                continue

            else:
                break

        currentValues = ValueResponseModel(**response_data)

        self.isOnline = not currentValues.IsOffline

        results = []

        for value in currentValues.Values:
            value = ValueModel(**value)  # type: ignore
            id = value.VariableId
            enumerator = Variable(id)
            name = enumerator.name

            # Regular expression pattern to match numeric value and unit
            pattern = r'^(-?[\d]+(?:[.,]\d{1,})?)(\D*)$'

            match = re.match(pattern, value.CurrentValue)
            if match:
                value = match.group(1)  # Extract the numeric value
                unit = match.group(2)  # Extract the unit
                if unit == "":
                    unit = None

            else:
                # If no match, consider the entire value as the value itself
                value = value.CurrentValue
                unit = None

            results.append(VariableValue(id, name, enumerator, value, unit))

        return results

    def get_history_values(self, variable: Variable, startDate: datetime, stopDate: datetime, resolution: int = 1000, force_login: bool = False) -> List[VariableHistoryValue]:
        """
        Returns history values for selected variable from specified timerange.
        """

        url = self._BASE_URL + '/PrivateAPI/History'

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'hpid': self._config.heatpump_id,
            'variableId': variable.value,
            'resolution': resolution,
            'startDate': int(startDate.timestamp()),
            'stopDate': int(stopDate.timestamp()),
            'isFullZoom': True,
            'reloadOverview': True
        }

        if not '.ASPXAUTH' in self._session.cookies and force_login:
            self._login()

        if not '.ASPXAUTH' in self._session.cookies:
            raise NotLoggedIn(
                "Session is not currenly logged in. Use force_login = True if you want to force relogin.")

        response = self._session.post(url, headers=headers, data=data)

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Request failed with status code {response.status_code}, data: {response}")

        try:
            response_data = HistoryResponseModel(**response.json())

        except requests.exceptions.JSONDecodeError:
            raise ResponseError(
                f"Cannot parse response data. Data: {response.content}")

        results = []

        for value in response_data.data:
            history_value = value[1]
            history_date = datetime.fromtimestamp(value[0]/1000)

            if response_data.unit == "":
                history_unit = None
            else:
                history_unit = response_data.unit

            results.append(VariableHistoryValue(
                history_value, history_unit, history_date))

        return results

    def logout(self):
        url = self._BASE_URL + '/LogOut'

        response = self._session.get(url)
