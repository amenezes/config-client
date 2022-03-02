from config import http
from tests import conftest


def test_get(monkeypatch):
    monkeypatch.setattr(http, "get", conftest.config_mock)
    resp = http.get("http://localhost:8888/test_app/development/master")
    assert resp.ok


def test_post(monkeypatch):
    monkeypatch.setattr(http, "post", conftest.oauth2_mock)
    resp = http.post("http://localhost:8888/oauth/token")
    assert resp.ok
