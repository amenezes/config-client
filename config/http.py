import functools
import typing

import requests


def _req(fnc: typing.Callable, uri: str, **kwargs) -> requests.Response:
    response: requests.Response = fnc(uri, **kwargs)
    response.raise_for_status()
    return response


get = functools.partial(_req, requests.get)
post = functools.partial(_req, requests.post)
