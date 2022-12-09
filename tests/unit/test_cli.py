import pytest

from config import __version__, http
from config.cli import cli, client, decrypt, encrypt
from config.spring import ConfigClient
from tests import conftest

SAMPLE_CONFIG = {"db": {"user": "root", "pass": "123"}}


def test_base_command(cli_runner):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.output == f"cli, version {__version__}\n"


class TestClientCommand:
    def get_config_mock(self, *args, **kwargs):
        return SAMPLE_CONFIG

    def dumb_func(self, *args, **kwargs):
        return True

    @pytest.fixture
    def connection_mock(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "get_config", self.dumb_func)

    @pytest.fixture
    def config_mock(self, connection_mock, monkeypatch):
        monkeypatch.setattr(ConfigClient, "config", SAMPLE_CONFIG)

    @pytest.fixture
    def attribute_mock(self, connection_mock, monkeypatch):
        monkeypatch.setattr(ConfigClient, "get", self.get_config_mock)

    def test_show_all_config(self, cli_runner, config_mock):
        result = cli_runner.invoke(client, ["app"])
        assert result.output is not None
        assert len(result.output) >= 100

    def test_show_filter_config(self, cli_runner, attribute_mock):
        result = cli_runner.invoke(client, ["app", "-f db"])
        assert "report for filter: ' db'" in result.output

    def test_connection_error(self, cli_runner):
        result = cli_runner.invoke(client, ["app"])
        assert result.output == "Error: 💥 Failed to contact server!\n"
        assert result.exit_code == 1

    def test_empty_response(self, cli_runner, config_mock):
        result = cli_runner.invoke(client, ["app", "-f xxx"])
        assert "No result found for filter: ' xxx'" in result.output
        assert result.exit_code == 0

    def test_save_as_json(self, cli_runner, attribute_mock):
        result = cli_runner.invoke(client, ["app", "-f db", "--json"])
        assert result.output == "File saved: response.json\n"
        assert result.exit_code == 0

    def test_custom_url_via_env(self, cli_runner, monkeypatch):
        monkeypatch.setenv("CONFIGSERVER_ADDRESS", "http://my-custom-server")
        monkeypatch.setattr(ConfigClient, "get_config", self.dumb_func)
        result = cli_runner.invoke(client, ["app", "-f db", "-v"])
        assert result.exit_code == 0
        assert "address: http://my-custom-server" in result.output

    def test_get_file(self, cli_runner, monkeypatch):
        monkeypatch.setattr(http, "get", conftest.text_mock)
        result = cli_runner.invoke(client, ["app", "--file", "nginx.conf"])
        assert result.output == "File saved: nginx.conf\n"
        assert result.exit_code == 0

    def test_get_file_error(self, cli_runner):
        result = cli_runner.invoke(client, ["app", "--file", "nginx.conf"])
        assert result.exit_code == 1
        assert result.output == "Error: 💥 Failed to contact server!\n"

    @pytest.mark.parametrize(
        "cmdline", ["app --auth user:pass", "app --digest user:pass"]
    )
    def test_get_config(self, cli_runner, cmdline, config_mock):
        result = cli_runner.invoke(client, cmdline.split())
        assert result.exit_code == 0
        assert result.output is not None
        assert len(result.output) >= 100

    @pytest.mark.parametrize(
        "cmdline",
        [
            "app --auth userpass",
            "app --auth user-pass",
            "app --digest user::pass",
            "app --digest user@pass",
        ],
    )
    def test_get_config_with_auth_error(self, cli_runner, cmdline):
        result = cli_runner.invoke(client, cmdline.split())
        assert result.exit_code == 1


class TestDecryptCommand:
    def _mock_decrypt(self, *args, **kwargs):
        return "123"

    def test_decrypt_command(self, cli_runner, monkeypatch):
        monkeypatch.setattr(ConfigClient, "decrypt", self._mock_decrypt)
        result = cli_runner.invoke(
            decrypt,
            ["dfa76862fe7f367d9c1923de55ba85512eea7a41163ade3059d64fcfbed31017"],
        )
        assert result.output is not None
        assert len(result.output) >= 100

    def test_decrypt_command_error(self, cli_runner, monkeypatch):
        monkeypatch.setattr(http, "post", SystemExit())
        result = cli_runner.invoke(
            decrypt,
            ["dfa76862fe7f367d9c1923de55ba85512eea7a41163ade3059d64fcfbed31017"],
        )
        result.exit_code == 1


class TestEncryptCommand:
    def _mock_encrypt(self, *args, **kwargs):
        return f"{conftest.ENCRYPTED_DATA}"

    def _mock_encrypt_raw(self, *args, **kwargs):
        return f"{{cipher}}{conftest.ENCRYPTED_DATA}"

    def test_encrypt_command(self, cli_runner, monkeypatch):
        monkeypatch.setattr(ConfigClient, "encrypt", self._mock_encrypt)
        result = cli_runner.invoke(encrypt, ["123"])
        assert result.output is not None
        assert r"{cipher}" not in result.output
        assert len(result.output) >= 100

    def test_encrypt_command_raw(self, cli_runner, monkeypatch):
        monkeypatch.setattr(ConfigClient, "encrypt", self._mock_encrypt_raw)
        result = cli_runner.invoke(encrypt, ["123", "--raw"])
        assert r"{cipher}" in result.output

    def test_encrypt_command_error(self, cli_runner):
        result = cli_runner.invoke(encrypt, ["123"])
        assert result.exit_code == 1
