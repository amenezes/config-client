"""Module for retrieve application's config from Spring Cloud Config."""
import logging
import os
import sys

from config.core import singleton

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


@singleton
class ConfigServer:
    """ConfigServer client."""

    _config = {}

    def __init__(self):
        """Create a instance to retrieve config from Spring Cloud Config."""
        self.__load_config_from_configserver()

    def __load_config_from_configserver(self):
        """Retrieve configuration information."""
        try:
            request_url = self.__format_configserver_url()
            response = requests.get(request_url)

            logging.debug(f"Response status code: {response.status_code}")

            if response.status_code == 200:
                self._config = response.json()

        except requests.exceptions.ConnectionError:
            logging.error(
                'Failed to establish connection with configserver.')
            sys.exit(1)

    def __format_configserver_url(self):
        """Format ConfigServer URL."""
        logging.debug('Building request URL')

        address = os.getenv('CONFIGSERVER_ADDRESS') or 'http://localhost:8888/configuration'
        branch = os.getenv('BRANCH') or 'master'
        profile = os.getenv('PROFILE') or 'development'
        context_name = os.getenv('APP_NAME')

        logging.debug(f"ConfigServer address: {address}")
        logging.debug(f"Branch configuration: {branch}")
        logging.debug(f"Profile set: {profile}")
        logging.debug(f"Configuration file base name: {context_name}")
        logging.debug(
            f"URL formatted: {address}/{branch}/{context_name}-{profile}.json")

        return f"{address}/{branch}/{context_name}-{profile}.json"

    @property
    def config(self):
        """Getter from configurations retrieved from configserver."""
        return self._config

    def get_attribute(self, attr):
        """Get attribute from configurations.

        Use <dot> to define a path on a key tree.
        """
        key_list = attr.split('.')
        logging.debug(f'Key attribute: {key_list}')

        attribute_content = self.config.get(key_list[0])
        logging.debug(f'Attribute content: {attribute_content}')

        for key in key_list[1:]:
            attribute_content = attribute_content.get(key)

        logging.debug(f"Configuration getted: {attribute_content}")

        return attribute_content

    def get_keys(self):
        """List all keys from configuration retrieved."""
        return self.config.keys()


def config_client(func):
    """Spring config client decorator."""
    def enable_config():
        """Inner function to create ConfigServer instance."""
        return func(ConfigServer())
    return enable_config
