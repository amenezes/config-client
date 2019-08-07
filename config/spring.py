"""Module for retrieve application's config from Spring Cloud Config."""
import json
import logging
import os
import sys
from urllib import request
from urllib.error import URLError

import attr

from config.core import singleton


logging.getLogger(__name__).addHandler(logging.NullHandler())


@singleton
@attr.s(slots=True)
class ConfigClient:
    """ConfigClient client."""

    address = attr.ib(
        type=str,
        default=os.getenv('CONFIGSERVER_ADDRESS'),
        converter=attr.converters.default_if_none(
            'http://localhost:8888/configuration'
        )
    )
    branch = attr.ib(
        type=str,
        default=os.getenv('BRANCH'),
        converter=attr.converters.default_if_none('master')
    )
    app_name = attr.ib(
        type=str,
        default=os.getenv('APP_NAME'),
        validator=attr.validators.instance_of(str)
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
    _config = attr.ib(
        type=dict,
        default={},
        init=False,
        validator=attr.validators.instance_of(dict)
    )

    def __attrs_post_init__(self):
        """Format ConfigClient URL."""
        self.url = self.url.format(
            address=self.address,
            app_name=self.app_name,
            branch=self.branch,
            profile=self.profile
        )
        if not self.url.endswith('.json'):
            self.url = self.url.replace(
                self.url[self.url.rfind('.'):], '.json'
            )
            logging.warning(
                'URL suffix adjusted to a supported format. '
                'For more details see: '
                'https://github.com/amenezes/config-client/#default-values'
            )
        logging.debug(f'Target URL configured: {self.url}')

    def get_config(self):
        """Retrieve configuration from Spring ConfigClient."""
        try:
            logging.debug(f'Requesting: {self.url}')

            response = request.urlopen(self.url)
            logging.debug(f'HTTP response code: {response.code}')
            if response.code == 200:
                self._config = json.loads(response.readlines()[0])
            else:
                raise Exception(
                    'Failed to retrieve the configurations. '
                    f'HTTP Response code: {response.status_code}.'
                )

        except URLError:
            logging.error(
                'Failed to establish connection with ConfigClient.'
            )
            sys.exit(1)

    @property
    def config(self):
        """Getter from configurations retrieved from ConfigClient."""
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


def config_client(*args, **kwargs):
    logging.debug(f'args: {args}')
    logging.debug(f'kwargs: {kwargs}')

    def wrap_function(function):
        logging.debug(f'caller: {function}')

        def enable_config():
            obj = ConfigClient(*args, **kwargs)
            obj.get_config()
            return function(obj)
        return enable_config
    return wrap_function
