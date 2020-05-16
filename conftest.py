import requests


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
        self.ok = kwargs.get('ok') or False
        self.status_code = kwargs.get('status_code') or 404
        self.raise_type = kwargs.get('raise_type') or False
        self.headers = {"Content-Type": "application/json"}
        self.text = kwargs.get('text', '')

    def raise_for_status(self):
        if self.raise_type == 'http_error':
            raise requests.exceptions.HTTPError()
        elif self.raise_type == 'system':
            raise SystemExit

    def json(self):
        return {"access_token": "eyJz93a...k4laUWw"}


def response_mock_success(*args, **kwargs):
    return ResponseMock(ok=True, status_code=202)


def response_mock_error(*args, **kwargs):
    return ResponseMock()


def response_mock_http_error(*args, **kwargs):
    return ResponseMock(raise_type='http_error')


def response_mock_system_error(*args, **kwargs):
    return ResponseMock(raise_type='system')

