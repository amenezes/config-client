import logging
from typing import Dict

import attr

import requests
from requests.auth import HTTPBasicAuth


logging.getLogger(__name__).addHandler(logging.NullHandler())


@attr.s(slots=True)
class OAuth2:

    access_token_uri = attr.ib(type=str)
    client_id = attr.ib(type=str)
    client_secret = attr.ib(type=str)
    grant_type = attr.ib(type=str, default="client_credentials")
    _token = attr.ib(type=str, default="", validator=attr.validators.instance_of(str))

    @property
    def token(self) -> str:
        return self._token

    def request_token(self, client_auth: HTTPBasicAuth, data: Dict[str, str]) -> None:
        try:
            response = requests.post(self.access_token_uri, auth=client_auth, data=data)
            if response.ok:
                self._token = response.json().get("access_token")
                logging.info("Access token successfully obtained.")
                logging.debug(f"access_token: {self._token}")
            else:
                raise Exception(
                    "Failed to retrieve oauth2 access_token. "
                    f"HTTP Response code: {response.status_code}."
                )
        except requests.exceptions.MissingSchema:
            logging.error("Access token URI it's empty")

    def configure(self) -> None:
        client_auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {"grant_type": f"{self.grant_type}"}
        self.request_token(client_auth, data)
