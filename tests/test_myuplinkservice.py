import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.pyupway.config import MyUpwayConfig
from src.pyupway.enums import Variable, DataService
from src.pyupway.services.myuplinkservice import MyUplinkService
from src.pyupway.exceptions import LoginErr
from src.pyupway.models import VariableValue


class TestMyUplinkService(unittest.TestCase):

    @patch('src.pyupway.services.myuplinkservice.requests.Session')
    def setUp(self, MockSession):
        # Mock the session and configure it
        self.mock_session = MockSession.return_value
        self.config = MyUpwayConfig(dataservice=DataService.MYUPLINK,
                                    client_id="test_client_id", client_secret="test_client_secret")
        self.service = MyUplinkService(config=self.config)

    @patch('src.pyupway.services.myuplinkservice.requests.post')
    def test_get_token(self, mock_post):
        # Mock the POST request to the token endpoint
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'mock_access_token'}
        mock_post.return_value = mock_response

        self.service._get_token()

        self.assertEqual(self.service._token, 'Bearer mock_access_token')
        self.assertEqual(
            self.service._session.headers['Authorization'], 'Bearer mock_access_token')

    @patch('src.pyupway.services.myuplinkservice.requests.Session.get')
    def test_login(self, mock_get):
        # Mock the GET request for login
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'systems': [{
                'devices': [{
                    'id': 'test_device_id',
                    'connectionState': 'Connected'
                }]
            }]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.service.login()

        self.assertEqual(self.service.deviceId, 'test_device_id')
        self.assertTrue(self.service.isOnline)

    @patch('src.pyupway.services.myuplinkservice.requests.Session.get')
    def test_get_current_values(self, mock_get):
        # Mock the GET request for current values
        mock_response = MagicMock()
        mock_response.json.return_value = [{
            "parameterId": 40067,
            "value": 21.5,
            "parameterUnit": "C",
            "enumValues": []
        }]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        variables = [Variable.AVG_OUTDOOR_TEMP]
        current_values = self.service.get_current_values(variables=variables)

        self.assertEqual(len(current_values), 1)
        self.assertEqual(current_values[0].Id, 40067)
        self.assertEqual(current_values[0].Value, 21.5)
        self.assertEqual(current_values[0].Unit, "C")

    @patch('src.pyupway.services.myuplinkservice.requests.Session.get')
    @patch('src.pyupway.services.myuplinkservice.requests.post')
    def test_get_current_values_with_token_refresh(self, mock_post, mock_get):
        # Mock GET request to return 401 Unauthorized initially, and 200 OK after token refresh
        mock_response_unauthorized = MagicMock()
        mock_response_unauthorized.status_code = 401
        mock_response_ok = MagicMock()
        mock_response_ok.status_code = 200
        mock_response_ok.json.return_value = [{
            "parameterId": 40067,
            "value": 21.5,
            "parameterUnit": "C",
            "enumValues": []
        }]
        mock_get.side_effect = [mock_response_unauthorized, mock_response_ok]

        # Mock POST request for token refresh
        mock_response_token = MagicMock()
        mock_response_token.status_code = 200
        mock_response_token.json.return_value = {
            'access_token': 'mock_access_token'}
        mock_post.return_value = mock_response_token

        variables = [Variable.AVG_OUTDOOR_TEMP]
        current_values = self.service.get_current_values(variables=variables)

        self.assertEqual(len(current_values), 1)
        self.assertEqual(current_values[0].Id, 40067)
        self.assertEqual(current_values[0].Value, 21.5)
        self.assertEqual(current_values[0].Unit, "C")

    # Test for get_history_values (method returns empty list)
    def test_get_history_values(self):
        variable = Variable.AVG_OUTDOOR_TEMP
        start_date = datetime(2022, 1, 1)
        stop_date = datetime(2022, 1, 2)
        resolution = 1000

        history_values = self.service.get_history_values(
            variable, start_date, stop_date, resolution)

        self.assertEqual(history_values, [])


if __name__ == '__main__':
    unittest.main()
