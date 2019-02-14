"""
Module for retrieve application's config from configserver
"""

import os
import sys
import requests

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())


class ConfigServer:
    """ConfigServer client"""

    _config = {}

    def __init__(self):
        self.__load_config_from_configserver()

    def __load_config_from_configserver(self):
        """
        Retrieves configuration information from the
        configuration server
        """
        try:
            logging.info('Retrieving config server configuration...')

            request_url = self.__format_configserver_url()
            response = requests.get(request_url)

            logging.debug(request_url)
            logging.debug('Response status code: %s' % response.status_code)

            if response.status_code == 200:
                self._config = response.json()

        except requests.exceptions.ConnectionError:
            logging.error(
                'Failed to establish connection with configserver.')
            sys.exit(1)

    def __format_configserver_url(self):
        """
        Set the URL to the format of the spring config server
        """
        logging.debug('Requesting configuration file')

        address = os.getenv(
            'CONFIGSERVER_ADDRESS') or 'http://localhost:8888/configuration'
        branch = os.getenv('BRANCH') or 'master'
        profile = os.getenv('PROFILE') or 'development'
        context_name = os.getenv('APP_NAME')

        return "%s/%s/%s-%s.json" % (address, branch, context_name, profile)

    @property
    def config(self):
        logging.debug('Getting atribute from content')
        return self._config
