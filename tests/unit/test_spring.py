"""Test spring module."""
import asyncio
from unittest.mock import PropertyMock

import pytest

from config import http
from config.exceptions import RequestFailedException
from config.spring import ConfigClient, config_client, create_config_client
from tests import conftest


def test_get_config(client, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    client.get_config()
    assert isinstance(client.config, dict)
    assert list(client.config) == ["health", "spring", "info", "server", "python"]


def test_get_config_async(client, monkeypatch):
    loop = asyncio.get_event_loop()
    monkeypatch.setattr(http, "get", conftest.config_mock)
    loop.run_until_complete(client.get_config_async())
    assert isinstance(client.config, dict)
    assert list(client.config) == ["health", "spring", "info", "server", "python"]


def test_get_config_failed(client):
    with pytest.raises(SystemExit):
        client.get_config()


def test_get_config_with_request_timeout(client, mocker):
    mocker.patch.object(http, "get", conftest.config_mock)
    spy = mocker.spy(http, "get")

    client.get_config(timeout=5.0, headers={"Accept": "application/json"})
    spy.assert_called_with(
        client.url, timeout=5.0, headers={"Accept": "application/json"}
    )


def test_get_config_response_failed(client):
    with pytest.raises(SystemExit):
        client.get_config()


def test_client_properties(client):
    assert isinstance(client.config, dict)
    assert isinstance(client.url, str)
    assert client.url == "http://localhost:8888/test_app/development/master"


def test_set_url_error(client):
    with pytest.raises(AttributeError):
        client.url = "http://localhost:8888/master/development-test_app.json"


def test_decorator_failed(client):
    @config_client(app_name="myapp")
    def inner(c=None):
        assert isinstance(c, ConfigClient)

    with pytest.raises(SystemExit):
        inner()


def test_decorator(client, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)

    @config_client(app_name="myapp")
    def inner(c=None):
        assert isinstance(c, ConfigClient)

    inner()


def test_decorator_wraps(client, monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)

    @config_client(app_name="myapp")
    def inner(c=None):
        return c

    assert inner.__name__ == "inner"


def test_decorator_pass_kwargs(client, mocker):
    mocker.patch.object(http, "get", conftest.config_mock)
    spy = mocker.spy(http, "get")

    @config_client(app_name="test_app", timeout=5)
    def inner(c):
        assert isinstance(c, ConfigClient)

    inner()
    spy.assert_called_with(
        f"{client.address}/{client.app_name}/{client.profile}/{client.label}",
        timeout=5,
    )


def test_fail_fast_disabled():
    client = ConfigClient(app_name="test_app", fail_fast=False)
    with pytest.raises(ConnectionError):
        client.get_config()


def test_create_config_client_with_singleton(monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    client1 = create_config_client(app_name="app1")
    client2 = create_config_client(app_name="app2")
    assert id(client1) == id(client2)


def test_keys(client):
    type(client)._config = PropertyMock(return_value=conftest.CONFIG)
    assert client.keys() == conftest.CONFIG.keys()


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("spring.cloud.consul.host", "discovery"),
        ("spring.cloud.consul.port", 8500),
        ("info.app.description", "pws test_app - development profile"),
        ("info.app.descriptions", ""),
    ],
)
def test_get(client, monkeypatch, expr, expected, mocker):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    client.get_config()
    assert client.get(expr) == expected


def test_get_file(client, monkeypatch, mocker):
    monkeypatch.setattr(http, "get", conftest.text_mock)
    spy = mocker.spy(http, "get")

    content = client.get_file("nginx.conf")
    spy.assert_called_with(f"{client.url}/nginx.conf")
    assert content == "some text"


def test_get_file_error(client):
    with pytest.raises(RequestFailedException):
        client.get_file("nginx.conf")


def test_encrypt_failed(client):
    with pytest.raises(RequestFailedException):
        client.encrypt("my-secret")


def test_decrypt_failed(client):
    with pytest.raises(RequestFailedException):
        client.decrypt(conftest.ENCRYPTED_DATA)


@pytest.mark.parametrize("path", ["/configuration/encrypt", "/encrypt"])
def test_encrypt(client, monkeypatch, mocker, path):
    monkeypatch.setattr(http, "post", conftest.encrypt_mock)
    spy = mocker.spy(http, "post")

    resp = client.encrypt("my-secret", path=path)
    spy.assert_called_with(
        uri=f"{client.address}{path}",
        data="my-secret",
        headers={"Content-Type": "text/plain"},
    )
    assert resp == conftest.ENCRYPTED_DATA


@pytest.mark.parametrize("path", ["/configuration/decrypt", "/decrypt"])
def test_decrypt(client, mocker, monkeypatch, path):
    monkeypatch.setattr(http, "post", conftest.decrypt_mock)
    spy = mocker.spy(http, "post")

    resp = client.decrypt(conftest.ENCRYPTED_DATA, path=path)
    spy.assert_called_with(
        uri=f"{client.address}{path}",
        data=conftest.ENCRYPTED_DATA,
        headers={"Content-Type": "text/plain"},
    )
    assert resp == "my-secret"


def test_client_with_auth(monkeypatch, mocker, oauth2):
    monkeypatch.setattr(http, "post", conftest.oauth2_mock)
    monkeypatch.setattr(http, "get", conftest.config_mock)
    spy = mocker.spy(http, "get")

    client = ConfigClient(app_name="test_app", oauth2=oauth2)
    client.get_config()
    spy.assert_called_with(
        client.url, headers={"Authorization": "Bearer eyJz93a...k4laUWw"}
    )


def test_client_with_auth_and_headers(monkeypatch, mocker, oauth2):
    monkeypatch.setattr(http, "post", conftest.oauth2_mock)
    monkeypatch.setattr(http, "get", conftest.config_mock)
    spy = mocker.spy(http, "get")

    client = ConfigClient(app_name="test_app", oauth2=oauth2)
    client.get_config(headers={"X-Client-ID": "test-client"}, verify=False)
    spy.assert_called_with(
        client.url,
        headers={
            "X-Client-ID": "test-client",
            "Authorization": "Bearer eyJz93a...k4laUWw",
        },
        verify=False,
    )


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"python.cache.timeout": 10}, {"python": {"cache": {"timeout": 10}}}),
        ({"health.config.enabled": False}, {"health": {"config": {"enabled": False}}}),
    ],
)
def test_to_dict(client, data, expected):
    assert client._to_dict(data) == expected


def test_merge_dict(client):
    first = {
        "info": {"description": "simple description", "docs": "http://localhost/docs"}
    }
    second = {"app": {"password": "234"}, "info": {"url": "http://localhost"}}
    expected = {
        "info": {
            "description": "simple description",
            "url": "http://localhost",
            "docs": "http://localhost/docs",
        },
        "app": {"password": "234"},
    }
    assert client._merge_dict(first, second) == expected
