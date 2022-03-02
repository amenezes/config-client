import pytest

from config import http
from config.auth import OAuth2
from config.cf import CF
from config.spring import ConfigClient
from tests import conftest


@pytest.fixture
def config_mock(mocker):
    def get_mock(*args, **kwargs):
        return {}

    mocker.patch("config.spring.ConfigClient.get_config", get_mock)


def configure_custom_client():
    custom_client = ConfigClient(
        address="http://localhost:8888/configuration", app_name="myapp"
    )
    custom_oauth2 = OAuth2(
        access_token_uri="http://localhost/token",
        client_id="id",
        client_secret="secret",
    )
    return CF(oauth2=custom_oauth2, client=custom_client)


def test_configure_custom_client():
    cf = configure_custom_client()
    assert cf.client.address == "http://localhost:8888/configuration"


def test_default_properties(cf):
    assert cf is not None


def test_vcap_services_property(cf):
    assert cf.vcap_services is not None


def test_vcap_application_property(cf):
    assert cf.vcap_application is not None


def test_get_config(cf, config_mock):
    cf.get_config()
    assert isinstance(cf.client.config, dict)


def test_config(cf):
    assert isinstance(cf.config, dict)


# @pytest.mark.parametrize(
#     "filter, expected",
#     [
#         ("", ""),
#         ("server.port", 8080),
#         ("info.app.password", "123")
#     ]
# )
def test_get(cf):
    assert cf.get("") == ""


def test_keys(cf):
    assert isinstance(list(cf.keys()), list)


def test_custom_properties(monkeypatch):
    monkeypatch.setattr(http, "post", conftest.oauth2_mock)
    oauth2 = OAuth2(
        access_token_uri="http://localhost/token",
        client_id="id",
        client_secret="secret",
    )
    client = ConfigClient(address="http://localhost", app_name="test_app")
    cf = CF(oauth2=oauth2, client=client)
    assert cf.client == client
    assert cf.oauth2 == oauth2
