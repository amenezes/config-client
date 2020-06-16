import pytest
from flask import Flask

import conftest
from config import requests
from config.ext.flask import FlaskConfig, _Config
from config.spring import ConfigClient


class TestSpring:
    @pytest.fixture
    def app(self):
        return Flask(__name__)

    @pytest.fixture
    def resp_mock(self, monkeypatch):
        monkeypatch.setattr(requests, "get", conftest.ResponseMock)

    def test_validate_error(self, app):
        with pytest.raises(TypeError):
            FlaskConfig(app, int)

    def test_integration_with_config_client(self, app, resp_mock):
        FlaskConfig(app)
        assert isinstance(app.config, _Config)

    def test_integration_with_config_client_inst(self, app, resp_mock):
        FlaskConfig(app, ConfigClient(app_name="myapp"))
        assert isinstance(app.config, _Config)

    def test_config_get(self, app, resp_mock):
        FlaskConfig(app)
        assert app.config.get("spring.cloud.consul.host") == "discovery"

    def test_config_direct_access(self, app, resp_mock):
        FlaskConfig(app)
        assert app.config["spring"]["cloud"]["consul"]["host"] == "discovery"
