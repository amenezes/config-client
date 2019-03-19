"""Module for retrieve application's config from Spring Cloud Config."""
import logging
import os
import sys

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


class ConfigServer:
    """ConfigServer client."""

    _config = {}

    def __init__(self):
        """Create a instance to retrieve config from Spring Cloud Config."""
        self.__load_config_from_configserver()

    def __load_config_from_configserver(self):
        """Retrieve configuration information."""
        try:
            logging.info('Retrieving config server configuration...')

            request_url = self.__format_configserver_url()
            response = requests.get(request_url)

            logging.debug(request_url)
            logging.debug(f"Response status code: {response.status_code}")

            if response.status_code == 200:
                self._config = response.json()

        except requests.exceptions.ConnectionError:
            logging.error('Failed to establish connection with configserver.')
            sys.exit(1)

    def __format_configserver_url(self):
        """Format ConfigServer URL."""
        logging.debug('Requesting configuration file')

        address = os.getenv('CONFIGSERVER_ADDRESS') or 'http://localhost:8888/configuration'
        branch = os.getenv('BRANCH') or 'master'
        profile = os.getenv('PROFILE') or 'development'
        context_name = os.getenv('APP_NAME')

        return f"{address}/{branch}/{context_name}-{profile}.json"

    @property
    def config(self):
        """Getter from configurations retrieved from configserver."""
        logging.debug('Getting atribute from content')
        return self._config

    def get_attribute(self, attr):
        """Get attribute from configurations.

        Use <dot> to define a path on a key tree.
        """
        key_list = attr.split('.')
        atribute_content = self._config.get(key_list[0])

        for key in key_list[1:]:
            atribute_content = atribute_content.get(key)

        logging.debug('Getting atribute from content')

        return atribute_content

    def get_keys(self):
        """List all keys from configuration retrieved."""
        logging.debug('Gettings keys from config file')

        return self.config().keys()
