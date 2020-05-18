import pytest
import requests

from config.auth import OAuth2
from config.exceptions import RequestTokenException


class ResponseMock:
    def __init__(self, *args, **kwargs):
        self.ok = True
        self.status_coede = 202

    def json(self):
        return {"access_token": "eyJz93a...k4laUWw"}


class ResponseMockError:
    def __init__(self, *args, **kwargs):
        self.ok = False
        self.status_code = 404


class TestOAuth2:
    @pytest.fixture
    def oauth2(self):
        return OAuth2(
            access_token_uri="https://p-spring-cloud-services.uaa.sys.example.com/oauth/token",
            client_id="p-config-server-example-client-id",
            client_secret="EXAMPLE_SECRET",
        )

    def test_token(self, oauth2):
        assert oauth2.token == ""

    def test_configure(self, oauth2, monkeypatch):
        monkeypatch.setattr(requests, "post", ResponseMock)
        oauth2.configure()
        assert oauth2.token is not None

    def test_configure_failed(self, oauth2, monkeypatch):
        monkeypatch.setattr(requests, "post", ResponseMockError)
        with pytest.raises(RequestTokenException):
            oauth2.configure()
