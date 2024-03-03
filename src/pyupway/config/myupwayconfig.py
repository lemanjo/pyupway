from __future__ import annotations
from typing import Optional
from ..enums import DataService
from ..exceptions import ConfigurationError


class MyUpwayConfig:
    username: Optional[str]
    password: Optional[str]
    heatpump_id: Optional[int]
    dataservice: DataService
    client_id: Optional[str]
    client_secret: Optional[str]

    def __init__(self, dataservice: DataService, username: str = None, password: str = None, heatpump_id: int = None, client_id: str = None, client_secret: str = None) -> None:
        self.dataservice = dataservice

        if self.dataservice == DataService.MYUPWAY:
            if not username:
                raise ConfigurationError("Username needs to be defined when using MyUpway")
            self.username = username

            if not password:
                raise ConfigurationError("Password needs to be defined when using MyUpway")
            self.password = password

            if not heatpump_id:
                raise ConfigurationError("Heatpump ID needs to be defined when using MyUpway")
            self.heatpump_id = heatpump_id
        
        if self.dataservice == DataService.MYUPLINK:
            if not client_id:
                raise ConfigurationError("Client id configuration is required for MyUplink")
            self.client_id = client_id

            if not client_secret:
                raise ConfigurationError("Client secret configuration is required for MyUplink")
            self.client_secret = client_secret