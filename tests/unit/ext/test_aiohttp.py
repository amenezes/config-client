import pytest
import requests
from aiohttp.web import Application

from config.ext.aiohttp import AioHttpConfig
from config.spring import ConfigClient
from tests.unit.test_spring import ResponseMock


class TestAioHttpIntegration:
    @pytest.fixture
    def app(self):
        return Application()

    @pytest.fixture
    def resp_mock(self, monkeypatch):
        monkeypatch.setattr(requests, "get", ResponseMock)

    def test_integration_with_config_client(self, app, resp_mock):
        AioHttpConfig(app)
        assert isinstance(app["config"], dict)

    def test_integration_with_config_client_inst(self, app, resp_mock):
        AioHttpConfig(app, client=ConfigClient(app_name="myapp"))
        assert isinstance(app["config"], dict)

    def test_config_get(self, app, resp_mock):
        AioHttpConfig(app)
        assert app["config"].get("spring.cloud.consul.host") == "discovery"

    def test_config_direct_access(self, app, resp_mock):
        AioHttpConfig(app)
        assert app["config"]["spring"]["cloud"]["consul"]["host"] == "discovery"

    def test_invalid_app(self):
        with pytest.raises(TypeError):
            AioHttpConfig(int)

    def test_invalid_client(self, app):
        with pytest.raises(TypeError):
            AioHttpConfig(app, client=int)
