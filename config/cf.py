import logging
import os

from config.auth import OAuth2
from config.spring import ConfigClient

import attr


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class CF:

    uri = attr.ib(
        type=str,
        default=os.getenv('VCAP_SERVICES.p-config-server.0.credentials.uri')
    )
    oauth2 = attr.ib(
        type=OAuth2,
        default=OAuth2()
    )
    client = attr.ib(
        type=ConfigClient,
        default=ConfigClient()
    )

    def __attrs_post_init__(self):
        self.oauth2.configure()
        if self.client.address == 'http://localhost:8888/configuration':
            self.client.address = self.uri

    def get_config(self):
        header = {f"Bearer {self.oauth2.token}"}
        return self.client.get_config(header)
