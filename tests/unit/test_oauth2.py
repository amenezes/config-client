import unittest
from unittest.mock import patch

from config.auth import OAuth2


class ResponseMock:
    def __init__(self, ok=True):
        self.ok = ok

    def json(self):
        return {
            'access_token': 'eyJz93a...k4laUWw'
        }


class TestOAuth2(unittest.TestCase):

    def setUp(self):
        self.oauth2 = OAuth2(
            access_token_uri='https://p-spring-cloud-services.uaa.sys.example.com/oauth/token',
            client_id='p-config-server-example-client-id',
            client_secret='EXAMPLE_SECRET'
        )

    def test_token(self):
        self.assertIsNone(self.oauth2.token)

    @patch('config.auth.requests.post')
    def test_configure(self, RequestsMock):
        self.oauth2.configure()
        self.assertIsNotNone(self.oauth2.token)

    @patch('config.auth.requests.post', return_value=ResponseMock(ok=False))
    def test_configure_failed(self, RequestsMock):
        with self.assertRaises(Exception):
            self.oauth2.configure()
