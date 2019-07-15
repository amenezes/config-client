"""Module for retrieve application's config from Spring Cloud Config."""
import logging
import os
import sys

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
        converter=attr.converters.default_if_none('ft-sdintegracoes-591')
    )
    app_name = attr.ib(
        type=str,
        default=os.getenv('APP_NAME'),
        converter=attr.converters.default_if_none('autosprocessuais-pecas-textos')
    )
    profile = attr.ib(
        type=str,
        default=os.getenv('PROFILE'),
        converter=attr.converters.default_if_none('development')
    )
    _url = attr.ib(default=None)
    _config = attr.ib(default={}, type=dict, init=False)

    def __attrs_post_init__(self):
       """Retrieve configuration information."""
       if self._url is None:
           self._url = f"{self.address}/{self.branch}/{self.app_name}-{self.profile}.json"

    def get_config(self):
        try:
            response = requests.get(self._url)
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
    
    @property
    def url(self):
        """Getter from ConfigServer URL."""
        return self._url

    def get_attribute(self, attr):
        """Get attribute from configurations.

        Use <dot> to define a path on a key tree.
        """
        key_list = attr.split('.')
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
    def enable_config(*args, **kwargs):
        """Inner function to create ConfigServer instance."""
        obj = ConfigServer(*args, **kwargs)
        obj.get_config()
        return func(obj)
    return enable_config
