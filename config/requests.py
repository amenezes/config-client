import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_STATUS_FORCELIST = (404, 500, 501, 502, 503, 504, 505)
DEFAULT_BACKOFF_FACTOR = 0.3
DEFAULT_RETRIES = 3


def http(
    retries=DEFAULT_RETRIES,
    backoff_factor=DEFAULT_BACKOFF_FACTOR,
    status_forcelist=DEFAULT_STATUS_FORCELIST,
    *args,
    **kwargs
) -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get(uri, **kwargs) -> Response:
    response = http().get(uri, **kwargs)
    return response
