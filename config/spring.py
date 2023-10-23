"""Module for retrieve application's config from Spring Cloud Config."""
import asyncio
import os
from functools import partial, wraps
from typing import Any, Callable, Dict, KeysView, Optional, Tuple

from attrs import converters, field, fields_dict, mutable, validators
from glom import glom

from . import http
from ._config import merge_dict, to_dict
from .auth import OAuth2
from .core import singleton
from .exceptions import RequestFailedException
from .logger import logger


@mutable
class ConfigClient:
    """Spring Cloud Config Client."""

    address: str = field(
        default=os.getenv("CONFIGSERVER_ADDRESS", "http://localhost:8888"),
        validator=validators.instance_of(str),
    )
    label: str = field(
        default=os.getenv("LABEL", "master"),
        validator=validators.instance_of(str),
    )
    app_name: str = field(
        default=os.getenv("APP_NAME", ""),
        validator=validators.instance_of(str),
    )
    profile: str = field(
        default=os.getenv("PROFILE", "development"),
        validator=validators.instance_of(str),
    )
    fail_fast: bool = field(  # type: ignore
        default=os.getenv("CONFIG_FAIL_FAST", True),
        validator=validators.instance_of(bool),
        converter=converters.to_bool,
    )
    oauth2: Optional[OAuth2] = field(
        default=None,
        validator=validators.optional(validators.instance_of(OAuth2)),
    )
    _config: dict = field(
        factory=dict,
        init=False,
        validator=validators.instance_of(dict),
        repr=False,
    )

    @property
    def url(self) -> str:
        """URL that will be used to request config."""
        return f"{self.address}/{self.app_name}/{self.profile}/{self.label}"

    def get_config(self, **kwargs) -> None:
        """Request the configuration to the config server.

        Usage:

        # Example 1:
        client.get_config()

        # Example 2:
        client.get_config(verify=False)

        :param kwargs: any keyword argument used to configure oauth2 or request for the server.
        """
        kwargs = self._configure_oauth2(**kwargs)
        try:
            response = http.get(self.url, **kwargs)
        except Exception as err:
            logger.error(f"Failed to request: {self.url}")
            logger.error(err)
            if self.fail_fast:
                logger.info("fail_fast enabled. Terminating process.")
                raise SystemExit("fail_fast enabled. Terminating process.")
            raise ConnectionError("fail_fast disabled.")
        fconfig = [
            to_dict(config)
            for config in reversed(
                glom(response.json(), ("propertySources", ["source"]))
            )
        ]
        server_config: dict = {}
        [merge_dict(server_config, c) for c in fconfig]
        merge_dict(self._config, server_config)

    async def get_config_async(self, **kwargs) -> None:
        """Request the configuration to the config server.

        Usage:

        # Example 1:
        await client.get_config_async()

        # Example 2:
        await client.get_config_async(verify=False)

        :param kwargs: any keyword argument used to configure oauth2 or request for the server.
        """
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, partial(self.get_config, **kwargs))

    def _configure_oauth2(self, **kwargs) -> dict:
        if self.oauth2:
            self.oauth2.configure(**kwargs)
            try:
                kwargs["headers"].update(self.oauth2.authorization_header)
            except KeyError:
                kwargs.update(dict(headers=self.oauth2.authorization_header))
        return kwargs

    def get_file(self, filename: str, **kwargs: dict) -> str:
        """Request a file from the config server.

        Usage:

        clieng.get_file('nginx.conf')


        :param filename: filename to retrieve from the server.
        :param kwargs: any keyword argument used to configure request for the server.
        """
        uri = f"{self.address}/{self.app_name}/{self.profile}/{self.label}/{filename}"
        try:
            response = http.get(uri, **kwargs)
        except Exception:
            raise RequestFailedException(f"{uri}")
        return response.text

    def encrypt(
        self,
        value: str,
        path: str = "/encrypt",
        headers: dict = {"Content-Type": "text/plain"},
        **kwargs: dict,
    ) -> str:
        """Request a encryption of a value to the config server.

        Usage:

        client.encrypt('123')


        :param value: value to encrypt.
        :param path: base URL to encrypt. [default=/encrypt].
        :param headers: HTTP Headers to send to server.
        :param kwargs: any keyword argument used to configure request for the server.
        """
        try:
            response = http.post(
                uri=f"{self.address}{path}", data=value, headers=headers, **kwargs
            )
        except Exception:
            raise RequestFailedException(f"{self.address}{path}")
        return response.text

    def decrypt(
        self,
        value: str,
        path: str = "/decrypt",
        headers: dict = {"Content-Type": "text/plain"},
        **kwargs: dict,
    ) -> str:
        """Request decryption from a value to the config server.

        Usage:

        client.decrypt('35a51fc974e5df6779265239624c4b404ababf08093d1ca265b19bed4863f038')


        :param value: value to decrypt.
        :param path: base URL to decrypt. [default=/decrypt].
        :param headers: HTTP Headers to send to server.
        :param kwargs: any keyword argument used to configure request for the server.
        """
        try:
            response = http.post(
                uri=f"{self.address}{path}", data=value, headers=headers, **kwargs
            )
        except Exception:
            raise RequestFailedException(f"{self.address}{path}")
        return response.text

    @property
    def config(self) -> dict:
        """Getter from configurations retrieved from ConfigClient."""
        return self._config

    def get(self, key: str, default: Any = "") -> Any:
        """Loads a configuration from a key.

        Usage:

        # Example 1:
        client.get('spring')

        # Exampel 2:
        client.get('spring.cloud.consul')


        :param key: configuration key.
        :param default: default value if key does not exist. [default=''].
        """
        return glom(self._config, key, default=default)

    def keys(self) -> KeysView:
        return self._config.keys()


@singleton
def create_config_client(**kwargs) -> ConfigClient:
    """
    Create ConfigClient singleton instance.

    Usage:

    # Example 1:
    client = create_config_client(app_name='simpleweb000')

    # Example 2:
    client = create_config_client(
        app_name='simpleweb000',
        address='http://localhost:8888/configuration'
    )

    :param address: Spring Cloud Config Server.
    :param label: branch used to retrieve configuration.
    :param app_name: application name.
    :param profile: config profile [default=development]
    :param fail_fast: enable fail_fast [default=True].
    :param oauth2: Spring Cloud Config Server.

    :return: ConfigClient instance.
    """
    instance_params, get_config_params = _get_params(**kwargs)
    obj = ConfigClient(**instance_params)
    obj.get_config(**get_config_params)
    return obj


def config_client(**kwargs) -> Callable[[Dict[str, str]], ConfigClient]:
    """ConfigClient decorator.

    Usage:

    # Example 1:
    @config_client(app_name='test')
    def get_config(config):
        db_user = config.get_attribute('database.user')


    # Example 2:
    @config_client(
        app_name='test',
        address='http://localhost:8888/configuration'
    )
    def get_config(config):
        db_user = config.get_attribute('database.user')


    :raises: ConnectionError: If fail_fast enabled.

    :return: ConfigClient instance.
    """
    instance_params, get_config_params = _get_params(**kwargs)

    def wrap_function(function):
        logger.debug(f"caller: [name='{function.__name__}']")

        @wraps(function)
        def enable_config():
            obj = ConfigClient(**instance_params)
            obj.get_config(**get_config_params)
            return function(obj)

        return enable_config

    return wrap_function


def _get_params(**kwargs) -> Tuple[Dict, Dict]:
    instance_params = {}
    get_config_params = {}
    for key, value in kwargs.items():
        if key in fields_dict(ConfigClient).keys():
            instance_params.update({key: value})
        else:
            get_config_params.update({key: value})
    logger.debug(
        f"params: [kwargs={kwargs}, instance={instance_params}, get_config={get_config_params}]"
    )
    return instance_params, get_config_params
