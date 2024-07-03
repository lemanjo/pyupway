from __future__ import annotations

import requests

from typing import List
from datetime import datetime

from ..config import MyUpwayConfig
from ..exceptions import LoginErr
from ..enums import Variable
from ..models import VariableValue, VariableHistoryValue

class MyUplinkService:
    _BASE_URL = 'https://api.myuplink.com'
    
    _config: MyUpwayConfig
    _session: requests.Session
    _token: str

    deviceId: str
    isOnline: bool

    def __init__(self, config: MyUpwayConfig) -> None:
        self._config = config
        self._session = requests.Session()

        self.login()
    
    def login(self):
        self._get_token()
    
        response = self._session.get(self._BASE_URL + '/v2/systems/me?page=1&itemsPerPage=10')
        response_data = response.json()

        device_data = response_data['systems'][0]['devices'][0]

        self.deviceId = device_data['id']
        self.isOnline = device_data['connectionState'] == "Connected"

    def get_current_values(self, variables: List[Variable] | None = None, force_login: bool = False) -> List[VariableValue]:
        """
        Returns current values for requested variables provided as list of VariableValue.
        If variables are not specified, function returns all variables.
        """

        params = {}

        if variables:
            params = {
                "parameters": ','.join(str(variable.value) for variable in variables)
            }
        
        response = self._session.get(self._BASE_URL + '/v2/devices/' + self.deviceId + '/points', params=params)

        if response.status_code == 401:
            self._get_token()

            response = self._session.get(self._BASE_URL + '/v2/devices/' + self.deviceId + '/points', params=params)

        elif response.status_code != 200:
            raise Exception(f"Failed to get values. API responded with status code {response.status_code}")

        response_data = response.json()

        results: List[VariableValue] = []

        for result in response_data:
            try:
                variableEnum = Variable(int(result["parameterId"]))
            except ValueError:
                print(f"ERROR: Missing Variable enum. Contact the maintainer (https://github.com/lemanjo/pyupway) to add it to the code with these details: {result}")
                continue

            raw_value = result["value"]
            # JSON does not distinguish between int and float, so python always outputs float. But enum
            # interpretation needs to be able to access the value as an int if it is one.
            value = int(raw_value) if raw_value.is_integer() else raw_value
            str_value = str(value)

            found_enum = [el for el in result["enumValues"] if str(el["value"]) == str_value]
            enum_value = found_enum[0]["text"] if len(found_enum) > 0 and "text" in found_enum[0] else str_value

            variable_value = VariableValue(
                Id=variableEnum.value,
                Name=variableEnum.name,
                Value=raw_value,
                Unit=result["parameterUnit"],
                EnumValue=enum_value,
                Enumerator=variableEnum
            )

            if not self._contains_variable_value_with_id(results, variable_value.Id):
                results.append(variable_value)
        
        return results

    def get_history_values(self, variable: Variable, startDate: datetime, stopDate: datetime, resolution: int = 1000, force_login: bool = False) -> List[VariableHistoryValue]:
        """
        No way to implement in new API.
        """

        results: List[VariableHistoryValue] = []

        return results
    
    def logout(self):
        """ No implementation """
        pass

    
    def _get_token(self):
        """
        Fetch new token from OAUTH
        """
        
        # Define token request parameters
        token_params = {
            'grant_type': 'client_credentials',  # or other grant type depending on your OAuth flow
            'client_id': self._config.client_id,
            'client_secret': self._config.client_secret,
            # additional parameters if needed
        }

        # Make a POST request to the token endpoint
        response = requests.post(self._BASE_URL+'/oauth/token', data=token_params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the token from the response
            token_data = response.json()
            access_token = "Bearer "+token_data['access_token']
            self._token = access_token
            self._session.headers.update({'Authorization': access_token})
        else:
            raise LoginErr("Cannot fetch MyUplink token")
    
    def _contains_variable_value_with_id(self, variable_values, Id):
        for var_value in variable_values:
            if var_value.Id == Id:
                return True
        return False
