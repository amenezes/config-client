import unittest
from unittest.mock import patch

from config.cf import CF
from config.spring import ConfigClient


class TestCF(unittest.TestCase):

    @patch('config.auth.OAuth2')
    def setUp(self, MockOAuth2):
        self.cf = CF(oauth2=MockOAuth2)

    @patch('config.spring.ConfigClient.get_config', return_value={})
    def test_get_config(self, ClientMock):
        self.cf.get_config()
        self.assertIsInstance(self.cf.client.config, dict)

    @patch('config.auth.OAuth2')
    def configure_custom_client(self, MockOAuth2):
        custom_client = ConfigClient()
        return CF(oauth2=MockOAuth2, client=custom_client)

    def test_custom_client(self):
        cf = self.configure_custom_client()
        self.assertEqual(cf.client.address, None)
