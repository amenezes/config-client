from attrs import field, mutable, validators
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, MissingSchema

from . import http
from .exceptions import RequestFailedException, RequestTokenException
from .logger import logger


@mutable
class OAuth2:
    access_token_uri: str = field(validator=validators.instance_of(str))
    client_id: str = field(validator=validators.instance_of(str))
    client_secret: str = field(validator=validators.instance_of(str))
    grant_type: str = field(
        default="client_credentials",
        validator=validators.instance_of(str),
    )
    _token: str = field(factory=str, validator=validators.instance_of(str), repr=False)

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value) -> None:
        self._token = value
        logger.debug(f"set: [access_token='{self._token}']")

    @property
    def authorization_header(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def request_token(self, client_auth: HTTPBasicAuth, data: dict, **kwargs) -> None:
        try:
            response = http.post(
                self.access_token_uri, auth=client_auth, data=data, **kwargs
            )
        except MissingSchema:
            raise RequestFailedException("Access token URL it's empty")
        except HTTPError:
            raise RequestTokenException("Failed to retrieve oauth2 access_token.")
        self.token = response.json().get("access_token")
        logger.info("Access token successfully obtained.")

    def configure(self, **kwargs) -> None:
        client_auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {"grant_type": f"{self.grant_type}"}
        self.request_token(client_auth, data, **kwargs)
