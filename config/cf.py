from typing import Any, Dict, KeysView

from attrs import field, mutable, validators

from .auth import OAuth2
from .cfenv import CFenv
from .spring import ConfigClient


@mutable
class CF:
    cfenv: CFenv = field(
        factory=CFenv,
        validator=validators.instance_of(CFenv),
    )
    oauth2: OAuth2 = field(default=None)
    client: ConfigClient = field(default=None)

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
                oauth2=self.oauth2,
            )

    @property
    def vcap_services(self):
        return self.cfenv.vcap_services

    @property
    def vcap_application(self):
        return self.cfenv.vcap_application

    def get_config(self, **kwargs) -> None:
        """Request the configuration to the config server.

        Usage:

        # Example 1:
        cf.get_config()

        # Example 2:
        cf.get_config(verify=False)

        :param kwargs: any keyword argument used to configure oauth2 or request for the server.
        """
        self.client.get_config(**kwargs)

    async def get_config_async(self, **kwargs) -> None:
        """Request the configuration to the config server.

        Usage:

        # Example 1:
        await cf.get_config_async()

        # Example 2:
        await cf.get_config_async(verify=False)

        :param kwargs: any keyword argument used to configure oauth2 or request for the server.
        """
        await self.client.get_config_async(**kwargs)

    @property
    def config(self) -> Dict:
        """Getter from configurations retrieved from ConfigClient."""
        return self.client.config

    def get(self, key: str, default: Any = "") -> Any:
        """Loads a configuration from a key.

        Usage:

        # Example 1:
        cf.get('spring')

        # Exampel 2:
        cf.get('spring.cloud.consul')


        :param key: configuration key.
        :param default: default value if key does not exist. [default=''].
        """
        return self.client.get(key, default)

    def keys(self) -> KeysView:
        return self.client.keys()
