"""Module for retrieve application's config from Spring Cloud Config."""
import asyncio
import os
from distutils.util import strtobool
from functools import partial, wraps
from typing import Any, Callable, Dict, KeysView, Optional, Tuple

from attrs import field, fields_dict, mutable, validators
from glom import glom

from . import http
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
    fail_fast: bool = field(
        default=bool(strtobool(str(os.getenv("CONFIG_FAIL_FAST", True)))),
        validator=validators.instance_of(bool),
        converter=bool,
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
        return f"{self.address}/{self.app_name}/{self.profile}/{self.label}"

    def get_config(self, **kwargs) -> None:
        """Request the configuration from the config server."""
        kwargs = self._configure_oauth2(**kwargs)
        try:
            response = http.get(self.url, **kwargs)
        except Exception as err:
            logger.error(f"Failed to request: {self.url}")
            logger.error(err)
            if self.fail_fast:
                logger.info("fail_fast enabled. Terminating process.")
                raise SystemExit(1)
            raise ConnectionError("fail_fast disabled.")
        fconfig = [
            self._to_dict(config)
            for config in reversed(
                glom(response.json(), ("propertySources", ["source"]))
            )
        ]
        server_config: dict = {}
        [self._merge_dict(server_config, c) for c in fconfig]
        self._merge_dict(self._config, server_config)

    async def get_config_async(self, **kwargs) -> None:
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

    def _to_dict(self, config: dict) -> dict:
        final_config: dict = {}
        for k, v in config.items():
            tconfig = {}
            last_key = k.split(".")[-1:][0]
            for ksub in reversed(k.split(".")):
                if ksub == last_key:
                    tconfig = {ksub: v}
                else:
                    tconfig = {ksub: tconfig}
            self._merge_dict(final_config, tconfig)
        return final_config

    def _merge_dict(self, primary_config: dict, secondary_config: dict) -> dict:
        for k, v in primary_config.items():
            if isinstance(v, dict):
                if k in secondary_config and isinstance(secondary_config[k], dict):
                    self._merge_dict(primary_config[k], secondary_config[k])
            elif k in secondary_config:
                primary_config[k] = secondary_config[k]
        for k, v in secondary_config.items():
            if k not in primary_config:
                primary_config.update({k: v})
        return primary_config

    def get_file(self, filename: str, **kwargs: dict) -> str:
        """Request a file from the config server."""
        uri = f"{self.address}/{self.app_name}/{self.profile}/{self.label}/{filename}"
        try:
            response = http.get(uri, **kwargs)
        except Exception:
            raise RequestFailedException(f"Failed to request URI: {uri}")
        return response.text

    def encrypt(
        self,
        value: str,
        path: str = "/encrypt",
        headers: dict = {"Content-Type": "text/plain"},
        **kwargs: dict,
    ) -> str:
        """Request a encryption from a value to the config server."""
        try:
            response = http.post(
                uri=f"{self.address}{path}", data=value, headers=headers, **kwargs
            )
        except Exception:
            raise RequestFailedException(f"Failed to request URI: {self.address}{path}")
        return response.text

    def decrypt(
        self,
        value: str,
        path: str = "/decrypt",
        headers: dict = {"Content-Type": "text/plain"},
        **kwargs: dict,
    ) -> str:
        """Request a decryption from a value to the config server.."""
        try:
            response = http.post(
                uri=f"{self.address}{path}", data=value, headers=headers, **kwargs
            )
        except Exception:
            raise RequestFailedException(f"Failed to request URI: {self.address}{path}")
        return response.text

    @property
    def config(self) -> Dict:
        """Getter from configurations retrieved from ConfigClient."""
        return self._config

    def get(self, key: str, default: Any = "") -> Any:
        return glom(self._config, key, default=default)

    def keys(self) -> KeysView:
        return self._config.keys()


@singleton
def create_config_client(**kwargs) -> ConfigClient:
    """
    Create ConfigClient singleton instance.

    :param address:
    :param app_name:
    :param branch:
    :param fail_fast:
    :param profile:
    :param url:
    :return: ConfigClient instance.
    """
    instance_params, get_config_params = __get_params(**kwargs)
    obj = ConfigClient(**instance_params)
    obj.get_config(**get_config_params)
    return obj


def config_client(**kwargs) -> Callable[[Dict[str, str]], ConfigClient]:
    """ConfigClient decorator.

    Usage:

    @config_client(app_name='test')
    def get_config(config):
        db_user = config.get_attribute('database.user')

    :raises: ConnectionError: If fail_fast enabled.
    :return: ConfigClient instance.
    """
    instance_params, get_config_params = __get_params(**kwargs)

    def wrap_function(function):
        logger.debug(f"caller: [name='{function.__name__}']")

        @wraps(function)
        def enable_config():
            obj = ConfigClient(**instance_params)
            obj.get_config(**get_config_params)
            return function(obj)

        return enable_config

    return wrap_function


def __get_params(**kwargs) -> Tuple[Dict, Dict]:
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
