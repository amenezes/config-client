import pytest

from config import http
from config.auth import OAuth2
from config.cf import CF
from config.spring import ConfigClient
from tests.conftest import response_mock_success


class TestCF:
    @pytest.fixture
    def config_mock(self, mocker):
        def get_mock(self, *args, **kwargs):
            return {}

        mocker.patch("config.spring.ConfigClient.get_config", get_mock)

    def configure_custom_client(self):
        custom_client = ConfigClient(
            address="http://localhost:8888/configuration", app_name="myapp"
        )
        custom_oauth2 = OAuth2(
            access_token_uri="http://localhost/token",
            client_id="id",
            client_secret="secret",
        )
        return CF(oauth2=custom_oauth2, client=custom_client)

    def test_configure_custom_client(self):
        cf = self.configure_custom_client()
        assert cf.client.address == "http://localhost:8888/configuration"

    def test_default_properties(self, cf):
        assert cf is not None

    def test_vcap_services_property(self, cf):
        assert cf.vcap_services is not None

    def test_vcap_application_property(self, cf):
        assert cf.vcap_application is not None

    def test_get_config(self, cf, config_mock):
        cf.get_config()
        assert isinstance(cf.client.config, dict)

    def test_config(self, cf):
        assert isinstance(cf.config, dict)

    def test_get_attribute(self, cf):
        assert cf.get_attribute("") == ""

    def test_getitem(self, cf):
        assert cf.get("") == ""

    def test_get_keys(self, cf):
        assert isinstance(list(cf.get_keys()), list)

    def test_keys(self, cf):
        assert isinstance(list(cf.keys()), list)

    def test_custom_properties(self, monkeypatch):
        monkeypatch.setattr(http, "post", response_mock_success)
        oauth2 = OAuth2(
            access_token_uri="http://localhost/token",
            client_id="id",
            client_secret="secret",
        )
        client = ConfigClient(address="http://localhost", app_name="test_app")
        cf = CF(oauth2=oauth2, client=client)
        assert cf.client, client
        assert cf.oauth2, oauth2
