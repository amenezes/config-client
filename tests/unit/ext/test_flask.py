import pytest
from flask import Flask

from config import http
from config.ext.flask import FlaskConfig, _Config
from config.spring import ConfigClient
from tests import conftest


@pytest.fixture(scope="module")
def flask_app():
    return Flask(__name__)


def test_invalid_config_client(flask_app):
    with pytest.raises(TypeError):
        FlaskConfig(flask_app, int)


def test_config_client_integration_with_flask(flask_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    FlaskConfig(flask_app)
    assert isinstance(flask_app.config, _Config)


def test_custom_config_client_integration_with_flask(flask_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    FlaskConfig(flask_app, ConfigClient(app_name="myapp"))
    assert isinstance(flask_app.config, _Config)


def test_flask_get_config(flask_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    FlaskConfig(flask_app)
    assert flask_app.config.get("spring.cloud.consul.host") == "discovery"


def test_flask_get_config_dict(flask_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    FlaskConfig(flask_app)
    assert flask_app.config["spring"]["cloud"]["consul"]["host"] == "discovery"


def test_invalid_config_client_flask_app():
    with pytest.raises(TypeError):
        FlaskConfig(None)
