import pytest
from aiohttp.web import Application

from config import http
from config.ext.aiohttp import AioHttpConfig
from config.spring import ConfigClient
from tests import conftest


@pytest.fixture(scope="module")
def aiohttp_app():
    return Application()


def test_config_client_integration_with_aiohttp(aiohttp_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    AioHttpConfig(aiohttp_app)
    assert isinstance(aiohttp_app["config"], dict)


def test_custom_config_client_integration_with_aiohttp(aiohttp_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    AioHttpConfig(aiohttp_app, client=ConfigClient(app_name="myaiohttp_app"))
    assert isinstance(aiohttp_app["config"], dict)


def test_aiohttp_get_config(aiohttp_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    AioHttpConfig(aiohttp_app)
    assert aiohttp_app["config"].get("spring.cloud.consul.host") == "discovery"


def test_aiohttp_get_config_dict(aiohttp_app, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    AioHttpConfig(aiohttp_app)
    assert aiohttp_app["config"]["spring"]["cloud"]["consul"]["host"] == "discovery"


def test_invalid_aiohttp_app():
    with pytest.raises(TypeError):
        AioHttpConfig(int)


def test_invalid_config_client_aiohttp_app(aiohttp_app):
    with pytest.raises(TypeError):
        AioHttpConfig(aiohttp_app, client=int)
