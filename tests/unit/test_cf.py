import unittest
from unittest.mock import patch

from config.auth import OAuth2
from config.cf import CF
from config.spring import ConfigClient


class TestCF(unittest.TestCase):
    def setUp(self):
        self.cf = CF()

    @patch("config.spring.ConfigClient.get_config", return_value={})
    def test_get_config(self, ClientMock):
        self.cf.get_config()
        self.assertIsInstance(self.cf.client.config, dict)

    @patch("config.auth.requests")
    def configure_custom_client(self, MockRequests):
        custom_client = ConfigClient(
            address="http://localhost:8888/configuration", app_name="myapp"
        )
        custom_oauth2 = OAuth2(
            access_token_uri="http://localhost/token",
            client_id="id",
            client_secret="secret",
        )
        return CF(oauth2=custom_oauth2, client=custom_client)

    def test_custom_client(self):
        cf = self.configure_custom_client()
        self.assertEqual(cf.client.address, "http://localhost:8888/configuration")

    def test_default_properties(self):
        self.cf

    def test_vcap_services_property(self):
        self.assertIsNotNone(self.cf.vcap_services)

    def test_vcap_application_property(self):
        self.assertIsNotNone(self.cf.vcap_application)

    def test_cf_config(self):
        self.assertIsInstance(self.cf.config, dict)

    def test_cf_get_attribute(self):
        self.assertEqual(self.cf.get_attribute(""), "")

    def test_cf_get_keys(self):
        self.assertEqual(list(self.cf.get_keys()), [])

    @unittest.skip
    def test_custom_properties(self):
        oauth2 = OAuth2(
            access_token_uri="http://localhost/token",
            client_id="id",
            client_secret="secret",
        )
        client = ConfigClient(address="http://localhost", app_name="test_app")
        cf = CF(oauth2=oauth2, client=client)
        self.assertEqual(cf.client, client)
        self.assertEqual(cf.oauth2, oauth2)
