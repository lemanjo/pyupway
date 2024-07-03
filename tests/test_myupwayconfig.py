import pytest
from src.pyupway.config.myupwayconfig import MyUpwayConfig
from src.pyupway.enums import DataService
from src.pyupway.exceptions import ConfigurationError


def test_myupwayconfig_myupway_success():
    # Test correct initialization for MyUpway
    config = MyUpwayConfig(
        dataservice=DataService.MYUPWAY,
        username="test_user",
        password="test_pass",
        heatpump_id=123
    )
    assert config.username == "test_user"
    assert config.password == "test_pass"
    assert config.heatpump_id == 123


def test_myupwayconfig_myuplink_success():
    # Test correct initialization for MyUplink
    config = MyUpwayConfig(
        dataservice=DataService.MYUPLINK,
        client_id="client_id",
        client_secret="client_secret"
    )
    assert config.client_id == "client_id"
    assert config.client_secret == "client_secret"


def test_myupwayconfig_missing_username():
    # Test missing username for MyUpway
    with pytest.raises(ConfigurationError, match="Username needs to be defined when using MyUpway"):
        MyUpwayConfig(
            dataservice=DataService.MYUPWAY,
            password="test_pass",
            heatpump_id=123
        )


def test_myupwayconfig_missing_password():
    # Test missing password for MyUpway
    with pytest.raises(ConfigurationError, match="Password needs to be defined when using MyUpway"):
        MyUpwayConfig(
            dataservice=DataService.MYUPWAY,
            username="test_user",
            heatpump_id=123
        )


def test_myupwayconfig_missing_heatpump_id():
    # Test missing heatpump_id for MyUpway
    with pytest.raises(ConfigurationError, match="Heatpump ID needs to be defined when using MyUpway"):
        MyUpwayConfig(
            dataservice=DataService.MYUPWAY,
            username="test_user",
            password="test_pass"
        )


def test_myupwayconfig_missing_client_id():
    # Test missing client_id for MyUplink
    with pytest.raises(ConfigurationError, match="Client id configuration is required for MyUplink"):
        MyUpwayConfig(
            dataservice=DataService.MYUPLINK,
            client_secret="client_secret"
        )


def test_myupwayconfig_missing_client_secret():
    # Test missing client_secret for MyUplink
    with pytest.raises(ConfigurationError, match="Client secret configuration is required for MyUplink"):
        MyUpwayConfig(
            dataservice=DataService.MYUPLINK,
            client_id="client_id"
        )
