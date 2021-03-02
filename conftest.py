import json

import requests

CUSTOM_VCAP_SERVICES = json.dumps(
    {
        "p-config-server": [
            {
                "credentials": {
                    "uri": "http://example_uri",
                    "access_token_uri": "http://example_access_token_uri",
                    "client_id": "example_client_id",
                    "client_secret": "example_client_secret",
                }
            }
        ]
    }
)


CUSTOM_VCAP_APPLICATION = json.dumps(
    {
        "application_name": "myapp",
        "space_name": "test",
        "organization_name": "test",
        "uris": [],
    }
)


CONFIG = {
    "health": {"config": {"enabled": False}},
    "spring": {
        "cloud": {
            "consul": {
                "discovery": {
                    "health-check-interval": "10s",
                    "health-check-path": "/manage/health",
                    "instance-id": "myapp:${random.value}",
                    "prefer-ip-address": True,
                    "register-health-check": True,
                },
                "host": "discovery",
                "port": 8500,
            }
        }
    },
}


class ResponseMock:
    def __init__(self, *args, **kwargs):
        self.ok = kwargs.get("ok") or False
        self.status_code = kwargs.get("status_code") or 404
        self.headers = {"Content-Type": "application/json"}
        self.text = kwargs.get("text", "")

    def json(self):
        return {"access_token": "eyJz93a...k4laUWw"}


def response_mock_success(*args, **kwargs):
    return ResponseMock(ok=True, status_code=202)


def response_mock_error(*args, **kwargs):
    return ResponseMock()


def connection_error(*args, **kwargs):
    raise ConnectionError


def value_error(*args, **kwargs):
    raise ValueError


def base_exception_error(*args, **kwargs):
    raise Exception


def system_error(*args, **kwargs):
    raise SystemExit


def http_error(*args, **kwargs):
    raise requests.exceptions.HTTPError


def missing_schema_error(*args, **kwargs):
    raise requests.exceptions.MissingSchema
