from typing import Any, Dict, KeysView

import attr

from config.auth import OAuth2
from config.cfenv import CFenv
from config.spring import ConfigClient


@attr.s(slots=True)
class CF:
    cfenv = attr.ib(
        type=CFenv, factory=CFenv, validator=attr.validators.instance_of(CFenv),
    )
    oauth2 = attr.ib(type=OAuth2, default=None)
    client = attr.ib(type=ConfigClient, default=None)

    def __attrs_post_init__(self) -> None:
        if not self.oauth2:
            self.oauth2 = OAuth2(
                access_token_uri=self.cfenv.configserver_access_token_uri(),
                client_id=self.cfenv.configserver_client_id(),
                client_secret=self.cfenv.configserver_client_secret(),
            )

        if not self.client:
            self.client = ConfigClient(
                address=self.cfenv.configserver_uri(),
                app_name=self.cfenv.application_name,
                profile=self.cfenv.space_name.lower(),
            )
        self.oauth2.configure()

    @property
    def vcap_services(self):
        return self.cfenv.vcap_services

    @property
    def vcap_application(self):
        return self.cfenv.vcap_application

    def get_config(self) -> None:
        header = {"Authorization": f"Bearer {self.oauth2.token}"}
        self.client.get_config(headers=header)

    @property
    def config(self) -> Dict:
        return self.client.config

    def get_attribute(self, value: str) -> Any:
        return self.client.get_attribute(value)

    def get_keys(self) -> KeysView:
        return self.client.get_keys()
