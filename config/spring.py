"""Module for retrieve application's config from Spring Cloud Config."""
import logging
import os
import sys
from functools import wraps

import attr

from config.core import singleton

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


@singleton
@attr.s
class ConfigServer:
    """ConfigServer client."""

    address = attr.ib(
        type=str,
        default=os.getenv('CONFIGSERVER_ADDRESS'),
        converter=attr.converters.default_if_none('http://localhost:8888/configuration')
    )
    branch = attr.ib(
        type=str,
        default=os.getenv('BRANCH'),
        converter=attr.converters.default_if_none('master')
    )
    app_name = attr.ib(
        type=str,
        default=os.getenv('APP_NAME'),
        converter=attr.converters.default_if_none('')
    )
    profile = attr.ib(
        type=str,
        default=os.getenv('PROFILE'),
        converter=attr.converters.default_if_none('development')
    )
    url = attr.ib(
        type=str,
        default="{address}/{branch}/{app_name}-{profile}.json"
    )
    _config = attr.ib(default={}, type=dict, init=False)

    def __attrs_post_init__(self):
        """Format ConfigServer URL."""
        self.url = self.url.format(
            address=self.address,
            app_name=self.app_name,
            branch=self.branch,
            profile=self.profile
        )

    def get_config(self):
        """Retrieve configuration from Spring Configserver."""
        try:
            response = requests.get(self.url)
            if response.ok:
                self._config = response.json()
            else:
                raise ValueError(
                    f'Response from: {self.url} was different than 200.')

        except requests.exceptions.ConnectionError:
            logging.error(
                'Failed to establish connection with configserver.')
            sys.exit(1)

    @property
    def config(self):
        """Getter from configurations retrieved from configserver."""
        return self._config

    def get_attribute(self, value):
        """Get attribute from configurations.

        Use <dot> to define a path on a key tree.
        """
        key_list = value.split('.')
        logging.debug(f'Key attribute: {key_list}')

        attribute_content = self._config.get(key_list[0])
        logging.debug(f'Attribute content: {attribute_content}')

        for key in key_list[1:]:
            attribute_content = attribute_content.get(key)

        logging.debug(f"Configuration getted: {attribute_content}")

        return attribute_content

    def get_keys(self):
        """List all keys from configuration retrieved."""
        return self._config.keys()


def config_client(func):
    """Spring config client decorator."""
    @wraps(func)
    def enable_config(*args, **kwargs):
        """Inner function to create ConfigServer instance."""
        obj = ConfigServer(*args, **kwargs)
        obj.get_config()
        return func(obj)
    return enable_config