import json
import logging
import os

import attr

from config.auth import OAuth2
from config.cloudfoundry import (
    default_vcap_application,
    default_vcap_services
)
from config.spring import ConfigClient

from glom import glom


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class CF:

    _vcap_services = json.loads(
        os.getenv('VCAP_SERVICES', default_vcap_services)
    )
    _vcap_application = json.loads(
        os.getenv('VCAP_APPLICATION', default_vcap_application)
    )
    _uri = glom(_vcap_services, 'p-config-server.0.credentials.uri')
    oauth2 = attr.ib(
        type=OAuth2,
        default=OAuth2(
            access_token_uri=glom(
                _vcap_services,
                'p-config-server.0.credentials.access_token_uri'
            ),
            client_id=glom(
                _vcap_services,
                'p-config-server.0.credentials.client_id'
            ),
            client_secret=glom(
                _vcap_services,
                'p-config-server.0.credentials.client_secret'
            )
        )
    )
    client = attr.ib(
        type=ConfigClient,
        default=ConfigClient(
            address=f"{_uri}",
            app_name=glom(_vcap_application, 'application_name')
        )
    )

    @property
    def vcap_services(self):
        return self._vcap_services

    @property
    def vcap_application(self):
        return self._vcap_application

    @property
    def uri(self):
        return self._uri

    def __attrs_post_init__(self):
        self.oauth2.configure()
        if self.client.address == 'http://localhost:8888':
            self.client.address = self.uri

    def get_config(self):
        header = {'Authorization': f"Bearer {self.oauth2.token}"}
        print(header)
        return self.client.get_config(header)

    @property
    def config(self):
        return self.client.config

    def get_attribute(self, value):
        return self.client.get_attribute(value)

    def get_keys(self):
        return self.client.get_keys()
