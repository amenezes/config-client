import json

import pytest
import requests
import requests_mock

from config.auth import OAuth2
from config.cf import CF
from config.cfenv import CFenv
from config.spring import ConfigClient

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
    "label": "master",
    "name": "test_app",
    "profiles": ["development"],
    "propertySources": [
        {
            "name": "https://github.com/amenezes/spring_config.git/test_app-development.yml",
            "source": {
                "info.app.description": "pws test_app - development profile",
                "info.app.name": "test_app",
                "python.cache.timeout": 10,
                "python.cache.type": "simple",
                "server.port": 8080,
            },
        },
        {
            "name": "https://github.com/amenezes/spring_config.git/test_app.yml",
            "source": {
                "info.app.description": "pws test_app",
                "info.app.name": "test_app",
                "info.app.password": "123",
                "server.port": 8080,
            },
        },
        {
            "name": "https://github.com/amenezes/spring_config.git/application.yml",
            "source": {
                "health.config.enabled": False,
                "spring.cloud.consul.host": "discovery",
                "spring.cloud.consul.port": 8500,
            },
        },
    ],
    "state": None,
    "version": "b478bb5c9784bb2285c461892fab22361007e0c9",
}

ENCRYPTED_DATA = "AQC4HPhv2tHW3irTDlFUQ7nBEuPiRiK/RNp0JOHfoS0MrgOxqUAYYnKo5YEu+lDOVm+8EKeRhuw8o+rPmSxDCiNZ7FrriFRAde4ZTJ45FTVzW6COFFEkuXJQktZ2dCqGKLeRrTwWQ98g0X7ee9nEsQXK40yKQRhPCXPFgLY9J0BEukn8i1omFtxSFJ0MGILt5n/Sen9/MOGp+yJXGw7FMLejBpVMc4m9rFDyTskyk8OiobbFfG/osAaNRc2R/cTDEHAXVJVw9QwMWp3EJKpOwnx1YVmL3+4msGLYtRpB0XSrGo2AbUNa+5xTwdXIehmIAbn/TckOJE4sBc6vTSjxmtkNcE9cLDC+nlH0ANR9r/9uPqNFErXWrUlbEMJQ9SU4XdU="


def config_mock(*args, **kwargs):
    URL = "http://localhost:8888/test_app/development/master"
    with requests_mock.Mocker() as m:
        m.get(URL, json=CONFIG)
        resp = requests.get(URL)
        return resp


def oauth2_mock(*args, **kwargs):
    URL = "https://p-spring-cloud-services.uaa.sys.example.com/oauth/token"
    with requests_mock.Mocker() as m:
        m.post(URL, json={"access_token": "eyJz93a...k4laUWw"})
        resp = requests.post(URL)
        return resp


def text_mock(*args, **kwargs):
    URL = "http://localhost:8888/test_app/development/master/nginx.conf"
    with requests_mock.Mocker() as m:
        m.get(URL, text="some text")
        resp = requests.get(URL)
        return resp


def encrypt_mock(*args, **kwargs):
    URL = "http://localhost:8888/configuration/encrypt"
    with requests_mock.Mocker() as m:
        m.post(URL, text=ENCRYPTED_DATA)
        resp = requests.post(URL)
        return resp


def decrypt_mock(*args, **kwargs):
    URL = "http://localhost:8888/configuration/decrypt"
    with requests_mock.Mocker() as m:
        m.post(URL, text="my-secret")
        resp = requests.post(URL)
        return resp


def oauth2_missing_schema_error(*args, **kwargs):
    URL = "https://p-spring-cloud-services.uaa.sys.example.com/oauth/token"
    with requests_mock.Mocker() as m:
        m.post(URL, exc=requests.exceptions.MissingSchema)
        requests.post(URL)


def connection_error(*args, **kwargs):
    raise ConnectionError


def value_error(*args, **kwargs):
    raise ValueError


def http_error(*args, **kwargs):
    with requests_mock.Mocker() as m:
        m.get(requests_mock.ANY, exc=requests.exceptions.HTTPError)
        requests.get("http://localhost:8888/ANY")


@pytest.fixture(scope="module")
def client():
    return ConfigClient(app_name="test_app")


@pytest.fixture(scope="module")
def oauth2():
    return OAuth2(
        access_token_uri="https://p-spring-cloud-services.uaa.sys.example.com/oauth/token",
        client_id="p-config-server-example-client-id",
        client_secret="EXAMPLE_SECRET",
    )


@pytest.fixture(scope="module")
def cfenv():
    return CFenv()


@pytest.fixture(scope="module")
def custom_cfenv():
    return CFenv(
        vcap_services=json.loads(CUSTOM_VCAP_SERVICES),
        vcap_application=json.loads(CUSTOM_VCAP_APPLICATION),
    )


@pytest.fixture(scope="module")
def cf():
    return CF()
