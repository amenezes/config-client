import pytest
from requests import HTTPError

from config import http


def test_get():
    resp = http.get("https://postman-echo.com/get")
    assert resp.ok


def test_get_error():
    with pytest.raises(HTTPError):
        http.get("https://postman-echo.com/status/404")


def test_post(monkeypatch):
    resp = http.post("https://postman-echo.com/post")
    assert resp.ok


def test_post_error():
    with pytest.raises(HTTPError):
        http.post("https://postman-echo.com/status/404")
