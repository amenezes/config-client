import pytest

from config.cfenv import CFenv


class TestCFEnv:
    @pytest.fixture
    def cfenv(self):
        return CFenv()

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
