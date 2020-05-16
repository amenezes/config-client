"""Test spring module."""
from unittest.mock import PropertyMock

import pytest
import requests

import conftest
from config.exceptions import RequestFailedException
from config.spring import ConfigClient, config_client, create_config_client


class TestConfigClient:
    @pytest.fixture
    def client(self, monkeypatch):
        return ConfigClient(app_name="test_app")

    def test_get_config(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", conftest.response_mock_success)
        client.get_config()
        assert isinstance(client.config, dict)

    def test_get_config_failed(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", conftest.response_mock_http_error)
        with pytest.raises(SystemExit):
            client.get_config()

    def test_get_config_with_request_timeout(self, client, mocker):
        TIMEOUT = 5.0
        mocker.patch.object(requests, "get")
        requests.get.return_value = conftest.ResponseMock()
        client.get_config(timeout=TIMEOUT, headers={"Accept": "application/json"})
        requests.get.assert_called_with(
            client.url, timeout=TIMEOUT, headers={"Accept": "application/json"}
        )

    def test_get_config_response_failed(self, client, monkeypatch):
        monkeypatch.setattr(requests, "get", conftest.response_mock_system_error)
        with pytest.raises(SystemExit):
            client.get_config()

    def test_config_property(self, client):
        assert isinstance(client.config, dict)

    def test_default_url_property(self, client):
        assert isinstance(client.url, str)
        assert client.url == "http://localhost:8888/master/test_app-development.json"

    def test_custom_url_property(self):
        client = ConfigClient(
            app_name="test_app", url="{address}/{branch}/{profile}-{app_name}.yaml",
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
        monkeypatch.setattr(requests, "get", conftest.response_mock_success)

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
        monkeypatch.setattr(requests, "get", conftest.response_mock_success)
        client1 = create_config_client(app_name="app1")
        client2 = create_config_client(app_name="app2")
        assert id(client1) == id(client2)

    def test_get_keys(self, client):
        type(client)._config = PropertyMock(return_value=conftest.CONFIG)
        assert client.get_keys() == conftest.CONFIG.keys()

    def test_get_attribute(self, client):
        type(client)._config = PropertyMock(return_value=conftest.CONFIG)
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

    def test_get_file_with_path(self, client, mocker):
        """ Should get file as plaintext """
        mocker.patch.object(requests, "get")
        requests.get.return_value = conftest.ResponseMock(text="some text")
        content = client.get_file("nginx.conf")
        requests.get.assert_called_with(
            f"{client.address}/{client.app_name}/{client.profile}/{client.branch}/nginx.conf"
        )
        assert content == "some text"
