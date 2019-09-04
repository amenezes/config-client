import logging
import os

import attr

import requests


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class OAuth2:

    access_token_uri = attr.ib(
        type=str,
        default=os.getenv(
            'VCAP_SERVICES.p-config-server.0.credentials.access_token_uri'
        )
    )
    client_id = attr.ib(
        type=str,
        default=os.getenv(
            'VCAP_SERVICES.p-config-server.0.credentials.client_id'
        )
    )
    client_secret = attr.ib(
        type=str,
        default=os.getenv(
            'VCAP_SERVICES.p-config-server.0.credentials.client_secret'
        )
    )
    grant_type = attr.ib(
        type=str,
        default='client_credentials'
    )
    _token = attr.ib(
        default=None
    )

    @property
    def token(self):
        return self._token

    def configure(self):
        client_auth = requests.auth.HTTPBasicAuth(
            self.client_id, self.client_secret
        )
        data = {
            'grant_type': f"{self.grant_type}"
        }
        response = requests.post(
            self.access_token_uri,
            auth=client_auth,
            data=data
        )
        if response.ok:
            self._token = response.json().get('access_token')
        else:
            raise Exception(
                'Failed to retrieve oauth2 access_token. '
                f'HTTP Response code: {response.status_code}.'
            )
