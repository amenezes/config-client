import pytest
from glom import Path

from config.cfenv import CFenv


def test_space_name(cfenv):
    assert cfenv.space_name is not None


def test_organization_name(cfenv):
    assert cfenv.organization_name is not None


def test_uris(cfenv):
    assert isinstance(cfenv.uris, list)


def test_configserver_uri(cfenv):
    assert cfenv.configserver_uri() is not None


def test_configserver_access_token_uri(cfenv):
    assert cfenv.configserver_access_token_uri() is not None


def test_configserver_client_id(cfenv):
    assert cfenv.configserver_client_id() is not None


def test_configserver_client_secret(cfenv):
    assert cfenv.configserver_client_secret() is not None


def test_default_vcap_service_prefix(cfenv):
    assert "p-config-server" in cfenv.vcap_services.keys()


@pytest.mark.parametrize("prefix", ["config-server", "p.config-server"])
def test_custom_vcap_service_prefix(prefix):
    cfenv2 = CFenv(vcap_service_prefix=prefix)
    assert prefix in cfenv2.vcap_services.keys()


def test_format_vcap_path(cfenv):
    path = cfenv._format_vcap_path("0.credentials.uri")
    assert path == Path("p-config-server", "0", "credentials", "uri")


def test_custom_vcap_configserver_uri(custom_cfenv):
    assert custom_cfenv.configserver_uri() == "http://example_uri"


def test_custom_vcap_configserver_access_token_uri(custom_cfenv):
    assert (
        custom_cfenv.configserver_access_token_uri()
        == "http://example_access_token_uri"  # noqa: W503
    )


def test_custom_vcap_configserver_client_id(custom_cfenv):
    assert custom_cfenv.configserver_client_id() == "example_client_id"


def test_custom_vcap_configserver_client_secret(custom_cfenv):
    assert custom_cfenv.configserver_client_secret() == "example_client_secret"
