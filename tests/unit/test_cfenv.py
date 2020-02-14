import unittest

from config.cfenv import CFenv


class TestCFenv(unittest.TestCase):

    def setUp(self):
        self.cfenv = CFenv()

    def test_space_name(self):
        self.assertEqual(self.cfenv.space_name, '')

    def test_organization_name(self):
        self.assertEqual(self.cfenv.organization_name, '')

    def test_uris(self):
        self.assertIsInstance(self.cfenv.uris, list)

    def test_configserver_uri(self):
        self.assertEqual(
            self.cfenv.configserver_uri(),
            ''
        )

    def test_configserver_access_token_uri(self):
        self.assertEqual(
            self.cfenv.configserver_access_token_uri(),
            ''
        )

    def test_configserver_client_id(self):
        self.assertEqual(
            self.cfenv.configserver_client_id(),
            ''
        )

    def test_configserver_client_secret(self):
        self.assertEqual(
            self.cfenv.configserver_client_secret(),
            ''
        )

    def test_default_vcap_service_prefix(self):
        self.assertIn('p-config-server', self.cfenv.vcap_services.keys())

    def test_custom_vcap_service_prefix(self):
        cfenv = CFenv(vcap_service_prefix='config-server')
        self.assertIn('config-server', cfenv.vcap_services.keys())
        self.assertNotEqual(self.cfenv.vcap_services, cfenv.vcap_services)

    def test_format_vcap_path(self):
        path = self.cfenv._format_vcap_path('.0.credentials.uri')
        self.assertEqual(path, 'p-config-server.0.credentials.uri')
