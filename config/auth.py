import attr
import requests
from requests.auth import HTTPBasicAuth

from config import logger
from config.exceptions import RequestFailedException, RequestTokenException


@attr.s(slots=True)
class OAuth2:
    access_token_uri = attr.ib(type=str, validator=attr.validators.instance_of(str))
    client_id = attr.ib(type=str, validator=attr.validators.instance_of(str))
    client_secret = attr.ib(type=str, validator=attr.validators.instance_of(str))
    grant_type = attr.ib(
        type=str,
        default="client_credentials",
        validator=attr.validators.instance_of(str),
    )
    _token = attr.ib(type=str, default="", validator=attr.validators.instance_of(str))

    @property
    def token(self) -> str:
        return self._token

    @property
    def authorization_header(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

    def request_token(self, client_auth: HTTPBasicAuth, data: dict) -> None:
        try:
            response = requests.post(self.access_token_uri, auth=client_auth, data=data)
            if response.ok:
                self._token = response.json().get("access_token")
                logger.info("Access token successfully obtained.")
                logger.debug(f"access_token: {self._token}")
            else:
                raise RequestTokenException(
                    "Failed to retrieve oauth2 access_token. "
                    f"HTTP Response code: {response.status_code}."
                )
        except requests.exceptions.MissingSchema as err:
            logger.error(err)
            raise RequestFailedException("Access token URI it's empty")

    def configure(self) -> None:
        client_auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {"grant_type": f"{self.grant_type}"}
        self.request_token(client_auth, data)
