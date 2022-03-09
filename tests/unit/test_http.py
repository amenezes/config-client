import pytest
from requests import HTTPError

from config import http


def test_get():
    resp = http.get("https://httpbin.org/get")
    assert resp.ok


def test_get_error():
    with pytest.raises(HTTPError):
        http.get("https://httpbin.org/status/404")


def test_post(monkeypatch):
    resp = http.post("https://httpbin.org/post")
    assert resp.ok


def test_post_error():
    with pytest.raises(HTTPError):
        http.post("https://httpbin.org/status/404")
