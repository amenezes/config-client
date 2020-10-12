import json

import pytest
from glom import Path

from config.cfenv import CFenv
from conftest import CUSTOM_VCAP_APPLICATION, CUSTOM_VCAP_SERVICES


class TestCFEnv:
    @pytest.fixture
    def cfenv(self):
        return CFenv()

    @pytest.fixture
    def custom_cfenv(self):
        return CFenv(
            vcap_services=json.loads(CUSTOM_VCAP_SERVICES),
            vcap_application=json.loads(CUSTOM_VCAP_APPLICATION),
        )

    def test_space_name(self, cfenv):
        assert cfenv.space_name == ""

    def test_organization_name(self, cfenv):
        assert cfenv.organization_name == ""

    def test_uris(self, cfenv):
        assert isinstance(cfenv.uris, list)

    def test_configserver_uri(self, cfenv):
        assert cfenv.configserver_uri() == ""

    def test_configserver_access_token_uri(self, cfenv):
        assert cfenv.configserver_access_token_uri() == ""

    def test_configserver_client_id(self, cfenv):
        assert cfenv.configserver_client_id() == ""

    def test_configserver_client_secret(self, cfenv):
        assert cfenv.configserver_client_secret() == ""

    def test_default_vcap_service_prefix(self, cfenv):
        assert "p-config-server" in cfenv.vcap_services.keys()

    @pytest.mark.parametrize("prefix", ["config-server", "p.config-server"])
    def test_custom_vcap_service_prefix(self, prefix):
        cfenv2 = CFenv(vcap_service_prefix=prefix)
        assert prefix in cfenv2.vcap_services.keys()

    def test_format_vcap_path(self, cfenv):
        path = cfenv._format_vcap_path("0.credentials.uri")
        assert path == Path("p-config-server", "0", "credentials", "uri")

    def test_custom_vcap_configserver_uri(self, custom_cfenv):
        assert custom_cfenv.configserver_uri() == "http://example_uri"

    def test_custom_vcap_configserver_access_token_uri(self, custom_cfenv):
        assert (
            custom_cfenv.configserver_access_token_uri()
            == "http://example_access_token_uri"  # noqa: W503
        )

    def test_custom_vcap_configserver_client_id(self, custom_cfenv):
        assert custom_cfenv.configserver_client_id() == "example_client_id"

    def test_custom_vcap_configserver_client_secret(self, custom_cfenv):
        assert custom_cfenv.configserver_client_secret() == "example_client_secret"
