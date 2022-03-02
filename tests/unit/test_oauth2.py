import pytest

from config import http
from config.exceptions import RequestFailedException, RequestTokenException
from tests import conftest


def test_token(oauth2):
    assert oauth2.token is not None


def test_configure(oauth2, monkeypatch):
    monkeypatch.setattr(http, "post", conftest.oauth2_mock)
    oauth2.configure()
    assert oauth2.token == "eyJz93a...k4laUWw"


def test_configure_failed(oauth2, monkeypatch):
    monkeypatch.setattr(http, "post", conftest.http_error)
    with pytest.raises(RequestTokenException):
        oauth2.configure()


def test_configure_request_failed(oauth2, monkeypatch):
    monkeypatch.setattr(http, "post", conftest.oauth2_missing_schema_error)
    with pytest.raises(RequestFailedException):
        oauth2.configure()


def test_authorization_header(oauth2, monkeypatch):
    monkeypatch.setattr(http, "post", conftest.oauth2_mock)
    oauth2.configure()
    assert isinstance(oauth2.authorization_header, dict)
