"""Module for retrieve application's config from Spring Cloud Config."""
import logging
import os
import sys
from typing import Any, Callable, Dict, KeysView

import attr

from config.core import singleton

from glom import glom

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class ConfigClient:
    """ConfigClient client."""

    address = attr.ib(
        type=str, default=os.getenv("CONFIGSERVER_ADDRESS", "http://localhost:8888")
    )
    branch = attr.ib(type=str, default=os.getenv("BRANCH", "master"))
    app_name = attr.ib(
        type=str,
        default=os.getenv("APP_NAME", ""),
        validator=attr.validators.instance_of(str),
    )
    profile = attr.ib(type=str, default=os.getenv("PROFILE", "development"))
    url = attr.ib(
        type=str,
        default="{address}/{branch}/{app_name}-{profile}.json"
    )
    _config = attr.ib(
        type=dict, default={}, init=False, validator=attr.validators.instance_of(dict)
    )

    def __attrs_post_init__(self) -> None:
        """Format ConfigClient URL."""
        self.url = self.url.format(
            address=self.address,
            app_name=self.app_name,
            branch=self.branch,
            profile=self.profile,
        )
        self._ensure_request_json()

    def _ensure_request_json(self) -> None:
        if not self.url.endswith(".json"):
            dot_position = self.url.rfind(".")
            if dot_position > 0:
                self.url = self.url.replace(self.url[dot_position:], ".json")
            else:
                self.url = f"{self.url}.json"
            logging.warning(
                "URL suffix adjusted to a supported format. "
                "For more details see: "
                "https://github.com/amenezes/config-client/#default-values"
            )
        logging.debug(f"Target URL configured: {self.url}")

    def get_config(self, headers: Dict = {}) -> None:
        """Retrieve configuration from Spring ConfigClient."""
        try:
            logging.debug(f"Requesting: {self.url}")

            response = requests.get(self.url, headers=headers)
            logging.debug(f"HTTP response code: {response.status_code}")
            if response.ok:
                self._config = response.json()
            else:
                raise Exception(
                    "Failed to retrieve the configurations. "
                    f"HTTP Response code: {response.status_code}."
                )

        except Exception:
            logging.error("Failed to establish connection with ConfigServer.")
            sys.exit(1)

    @property
    def config(self) -> Dict:
        """Getter from configurations retrieved from ConfigClient."""
        return self._config

    def get_attribute(self, value: str) -> Any:
        """Get attribute from configurations."""
        return glom(self._config, value, default="")

    def get_keys(self) -> KeysView:
        """List all keys from configuration retrieved."""
        return self._config.keys()


@singleton
def create_config_client(**kwargs):
    obj = ConfigClient(**kwargs)
    obj.get_config()
    return obj


def config_client(*args, **kwargs) -> Callable[[Dict[str, str]], ConfigClient]:
    logging.debug(f"args: {args}")
    logging.debug(f"kwargs: {kwargs}")

    def wrap_function(function):
        logging.debug(f"caller: {function}")

        def enable_config():
            obj = ConfigClient(*args, **kwargs)
            obj.get_config()
            return function(obj)

        return enable_config

    return wrap_function
