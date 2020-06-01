"""Module for retrieve application's config from Spring Cloud Config."""
import os
from distutils.util import strtobool
from os.path import isfile
from typing import Any, Callable, Dict, KeysView

import attr
import requests
import yaml
from glom import glom

from config import logger
from config.core import singleton
from config.exceptions import RequestFailedException
from config.utils import merge_dicts


@attr.s(slots=True)
class ConfigClient:
    """Spring Cloud Config Client."""

    timeout = attr.ib(
        type=int,
        default=int(os.getenv("CONFIG_TIMEOUT", 5)),
        validator=attr.validators.instance_of(int),
    )
    address = attr.ib(
        type=str,
        default=os.getenv("CONFIGSERVER_ADDRESS", "http://localhost:8888"),
        validator=attr.validators.instance_of(str),
    )
    branch = attr.ib(
        type=str,
        default=os.getenv("BRANCH", "master"),
        validator=attr.validators.instance_of(str),
    )
    app_name = attr.ib(
        type=str,
        default=os.getenv("APP_NAME", ""),
        validator=attr.validators.instance_of(str),
    )
    profile = attr.ib(
        type=str,
        default=os.getenv("PROFILE", "development"),
        validator=attr.validators.instance_of(str),
    )
    url = attr.ib(
        type=str,
        default="{address}/{branch}/{app_name}-{profile}.json",
        validator=attr.validators.instance_of(str),
    )
    fail_fast = attr.ib(
        type=bool,
        default=bool(strtobool(str(os.getenv("CONFIG_FAIL_FAST", True)))),
        validator=attr.validators.instance_of(bool),
    )
    _config = attr.ib(
        type=dict,
        factory=dict,
        init=False,
        validator=attr.validators.instance_of(dict),
        repr=False,
    )

    filename = attr.ib(type=str, validator=attr.validators.instance_of(str), init=False)

    config_file_path = attr.ib(
        type=str,
        default=os.getenv("CONFIG_FILE_PATH", "config/{profile}.yml"),
        validator=attr.validators.instance_of(str),
    )

    def __attrs_post_init__(self) -> None:
        """Format ConfigClient URL."""
        self.url = self.url.format(
            address=self.address,
            branch=self.branch,
            app_name=self.app_name,
            profile=self.profile,
        )
        self._ensure_request_json()

        self.filename = self.config_file_path.format(
            branch=self.branch, app_name=self.app_name, profile=self.profile
        )

    def _ensure_request_json(self) -> None:
        if not self.url.endswith(".json"):
            dot_position = self.url.rfind(".")
            if dot_position > 0:
                self.url = self.url.replace(self.url[dot_position:], ".json")
            else:
                self.url = f"{self.url}.json"
            logger.warning(
                "URL suffix adjusted to a supported format. "
                "For more details see: "
                "https://config-client.amenezes.net/docs/1.-overview/#default-values"
            )
        logger.debug(f"Target URL configured: {self.url}")

    def get_config(self, **kwargs: dict) -> None:
        try:
            self._config = dict(
                merge_dicts(
                    self.get_config_from_file(), self.get_config_from_server(**kwargs)
                )
            )
        except RequestFailedException:
            self._config = self.get_config_from_file()
            if not self._config:
                raise

    def get_config_from_server(self, **kwargs: dict) -> None:
        try:
            timeout = kwargs.pop("timeout", self.timeout)
            response = self._request(self.url, timeout=timeout, **kwargs)
        except Exception as ex:
            logger.error(f"Failed to request: {self.url}")
            logger.error(ex)
            if self.fail_fast:
                logger.info("fail_fast enabled. Terminating process.")
                raise SystemExit(1)
            raise ConnectionError("fail_fast disabled.")
        return response.json()

    def get_config_from_file(self):
        logger.debug("Using config file %s", self.filename)
        if not isfile(self.filename):
            logger.debug("%s does not found", self.filename)
            return {}
        return yaml.full_load(open(self.filename))

    def get_file(self, filename: str, **kwargs: dict) -> str:
        uri = f"{self.address}/{self.app_name}/{self.profile}/{self.branch}/{filename}"
        logger.debug(f"URI to request file: {uri}")
        try:
            response = self._request(uri, **kwargs)
        except Exception:
            logger.error(f"Failed to request URI: {uri}")
            raise RequestFailedException(f"Failed to request URI: {uri}")
        return response.text

    def _request(self, uri, **kwargs) -> requests.Response:
        response = requests.get(uri, **kwargs)
        response.raise_for_status()
        return response

    @property
    def config(self) -> Dict:
        """Getter from configurations retrieved from ConfigClient."""
        return self._config

    def get_attribute(self, value: str) -> Any:
        """
        Get attribute from configuration.

        :value value: -- The filter to query on dict.
        :return: The value matches or ''
        """
        return glom(self._config, value, default="")

    def get_keys(self) -> KeysView:
        """List all keys from configuration retrieved."""
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
    obj = ConfigClient(**kwargs)
    obj.get_config()
    return obj


def config_client(*args, **kwargs) -> Callable[[Dict[str, str]], ConfigClient]:
    """ConfigClient decorator.

    Usage:

    @config_client(app_name='test')
    def get_config(config):
        db_user = config.get_attribute('database.user')

    :raises: ConnectionError: If fail_fast enabled.
    :return: ConfigClient instance.
    """
    logger.debug(f"args: {args}")
    logger.debug(f"kwargs: {kwargs}")

    def wrap_function(function):
        logger.debug(f"caller: {function}")

        def enable_config():
            obj = ConfigClient(*args, **kwargs)
            obj.get_config()
            return function(obj)

        return enable_config

    return wrap_function
