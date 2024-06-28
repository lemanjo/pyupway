from __future__ import annotations

import requests
import re

from typing import List
from datetime import datetime

from ..config import MyUpwayConfig
from ..exceptions import LoginErr, NotLoggedIn, ResponseError
from ..models import ValueModel, VariableHistoryValue, VariableValue
from ..enums import Variable
from ..responses import ValueResponseModel, HistoryResponseModel

TIME_REPRESENTATION_FORMATS = [
    "%m/%d/%Y %H:%M:%S",
    "%Y. %m. %d. %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H.%M.%S"
]


class MyUpwayService:
    _DOMAIN = 'myupway.com'
    _BASE_URL = f'https://www.{_DOMAIN}'

    _config: MyUpwayConfig
    _session: requests.Session

    deviceId: str
    isOnline: bool

    def __init__(self, config: MyUpwayConfig) -> None:
        self._config = config
        self._session = requests.Session()
        # Set language to en to be able to get boolean values right
        self._session.cookies.set("EmilLanguage", "en-GB", domain=self._DOMAIN)

        self.deviceId = self._config.heatpump_id

        self.login()

    def login(self) -> None:

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
            raise LoginErr("Login failed.")

        self.get_current_values() # perform request to set the isOnline flag

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
            self.login()

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
            self.login()

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
