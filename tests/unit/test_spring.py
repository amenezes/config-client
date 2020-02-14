"""Test spring module."""
from unittest.mock import PropertyMock

import pytest
import requests

from config.exceptions import RequestFailedException
from config.spring import ConfigClient, config_client, create_config_client


class ResponseMock:
    CONFIG = {
        "health": {"config": {"enabled": False}},
        "spring": {
            "cloud": {
                "consul": {
                    "discovery": {
                        "health-check-interval": "10s",
                        "health-check-path": "/manage/health",
                        "instance-id": "pecas-textos:${random.value}",
                        "prefer-ip-address": True,
                        "register-health-check": True,
                    },
                    "host": "discovery",
                    "port": 8500,
                }
            }
        },
    }

    def __init__(self, *args, **kwargs):
        self.status_code = 200
        self.ok = True
        self.headers = {"Content-Type": "application/json"}

    def json(self):
        return self.CONFIG


class ResponseMockError:
    def __init__(self, *arsgs, **kwargs):
        self.ok = False
        self.status_code = 404


class TestConfigClient:
    CONFIG_EXAMPLE = {
        "health": {"config": {"enabled": False}},
        "spring": {
            "cloud": {
                "consul": {
                    "discovery": {
                        "health-check-interval": "10s",
                        "health-check-path": "/manage/health",
                        "instance-id": "pecas-textos:${random.value}",
                        "prefer-ip-address": True,
                        "register-health-check": True,
                    },
                    "host": "discovery",
                    "port": 8500,
                }
            }
        },
    }

    @pytest.fixture
    def client(self, monkeypatch):
        return ConfigClient(app_name="test_app")

    def test_get_config(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", ResponseMock)
        client.get_config()
        assert isinstance(client.config, dict)

    def test_get_config_failed(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", ResponseMockError)
        with pytest.raises(RequestFailedException):
            client.get_config()

    def test_get_config_response_failed(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", ResponseMock(code=404, ok=False))
        with pytest.raises(SystemExit):
            client.get_config()

    def test_config_property(self, client):
        assert isinstance(client.config, dict)

    def test_default_url_property(self, client):
        assert isinstance(client.url, str)
        assert client.url == "http://localhost:8888/master/test_app-development.json"

    def test_custom_url_property(self):
        client = ConfigClient(
            app_name="test_app", url="{address}/{branch}/{profile}-{app_name}.yaml"
        )
        assert client.url == "http://localhost:8888/master/development-test_app.json"

    def test_decorator_failed(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", Exception)

        @config_client(app_name="myapp")
        def inner(c=None):
            assert isinstance(c, ConfigClient)

        with pytest.raises(SystemExit):
            inner()

    def test_decorator(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", ResponseMock)

        @config_client(app_name="myapp")
        def inner(c=None):
            assert isinstance(c, ConfigClient)

        inner()

    def test_fail_fast_disabled(self, monkeypatch):
        monkeypatch.setattr(requests, "get", Exception)
        client = ConfigClient(app_name="test_app", fail_fast=False)
        with pytest.raises(ConnectionError):
            client.get_config()

    def test_create_config_client_with_singleton(self, monkeypatch):
        monkeypatch.setattr(requests, "get", ResponseMock)
        client1 = create_config_client(app_name="app1")
        client2 = create_config_client(app_name="app2")
        assert id(client1) == id(client2)

    def test_get_keys(self, client):
        type(client)._config = PropertyMock(return_value=self.CONFIG_EXAMPLE)
        assert client.get_keys() == self.CONFIG_EXAMPLE.keys()

    def test_get_attribute(self, client):
        type(client)._config = PropertyMock(return_value=self.CONFIG_EXAMPLE)
        response = client.get_attribute("spring.cloud.consul.host")
        assert response is not None
        assert response == "discovery"

    def test_fix_valid_url_extension(self, client):
        client.url == "http://localhost:8888/master/test-app-development.json"

    def test_fix_url_extension_without_profile(self):
        client = ConfigClient(
            app_name="simpleweb000", url="{address}/{branch}/{app_name}"
        )
        client.url == "http://localhost:8888/master/simpleweb000.json"
