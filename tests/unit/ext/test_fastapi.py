from unittest.mock import MagicMock

import pytest

from config import CF, ConfigClient, http
from config.ext.fastapi import fastapi_cloud_foundry, fastapi_config_client
from tests import conftest


class MockApp:
    """Mock de FastAPI app para testes."""

    def __init__(self):
        self._config_client = None

    @property
    def config_client(self):
        if self._config_client is not None:
            return self._config_client
        raise AttributeError("config_client not initialized")

    @config_client.setter
    def config_client(self, value):
        self._config_client = value


@pytest.fixture
def mock_request():
    """Cria mock de FastAPI Request com app attribute."""
    app = MockApp()
    request = MagicMock()
    request.app = app
    return request


@pytest.fixture
def mock_request_without_config_client(mock_request):
    """Cria mock de Request sem config_client inicializado."""
    return mock_request


@pytest.fixture
def mock_request_with_config_client(mock_request):
    """Cria mock de Request com config_client já inicializado."""
    mock_request.app.config_client = MagicMock()
    return mock_request


@pytest.mark.asyncio
async def test_fastapi_config_client_injection(
    mock_request_without_config_client, monkeypatch
):
    """Testa injeção do config_client no request.app."""
    monkeypatch.setattr(http, "get", conftest.config_mock)
    await fastapi_config_client(mock_request_without_config_client)
    assert hasattr(mock_request_without_config_client.app, "config_client")
    assert isinstance(
        mock_request_without_config_client.app.config_client, ConfigClient
    )


@pytest.mark.asyncio
async def test_fastapi_config_client_skip_reinit(
    mock_request_with_config_client, mocker
):
    """Testa que não recria o config_client se já existe."""
    spy = mocker.spy(http, "get")
    await fastapi_config_client(mock_request_with_config_client)
    spy.assert_not_called()
    assert isinstance(mock_request_with_config_client.app.config_client, MagicMock)


@pytest.mark.asyncio
async def test_fastapi_cloud_foundry_injection(
    mock_request_without_config_client, monkeypatch, mocker
):
    """Testa injeção do CF no request.app."""
    monkeypatch.setattr(ConfigClient, "get_config_async", lambda self, **kwargs: None)
    cf_mock = mocker.MagicMock(spec=CF)
    mocker.patch("config.ext.fastapi.CF", return_value=cf_mock)
    await fastapi_cloud_foundry(mock_request_without_config_client)
    assert hasattr(mock_request_without_config_client.app, "config_client")
    assert mock_request_without_config_client.app.config_client is cf_mock


@pytest.mark.asyncio
async def test_fastapi_cloud_foundry_skip_reinit(
    mock_request_with_config_client, mocker
):
    """Testa que não recria o config_client se já existe."""
    spy = mocker.spy(ConfigClient, "get_config_async")
    await fastapi_cloud_foundry(mock_request_with_config_client)
    spy.assert_not_called()
    assert isinstance(mock_request_with_config_client.app.config_client, MagicMock)


@pytest.mark.asyncio
async def test_fastapi_config_loaded_correctly(
    mock_request_without_config_client, monkeypatch
):
    """Testa que a config foi carregada corretamente."""
    monkeypatch.setattr(http, "get", conftest.config_mock)
    await fastapi_config_client(mock_request_without_config_client)
    client = mock_request_without_config_client.app.config_client
    assert client.get("spring.cloud.consul.host") == "discovery"
    assert client.get("info.app.name") == "test_app"
