import requests


def request(uri: str, **kwargs) -> requests.Response:
    response = requests.get(uri, **kwargs)
    response.raise_for_status()
    return response


def post(uri: str, data: str, **kwargs) -> requests.Response:
    response = requests.post(uri, data=data, **kwargs)
    response.raise_for_status()
    return response
