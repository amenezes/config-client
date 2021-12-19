import functools
import typing

import requests

from .logger import logger


def _req(fnc: typing.Callable, uri: str, **kwargs) -> requests.Response:
    logger.debug(
        f"HTTP Request: [type='{fnc.__name__}', uri='{uri}', kwargs='{kwargs}']"
    )
    response: requests.Response = fnc(uri, **kwargs)
    response.raise_for_status()
    return response


get = functools.partial(_req, requests.get)
post = functools.partial(_req, requests.post)
