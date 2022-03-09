import pytest
from cleo import Application, CommandTester

from config import http
from config.cli import ConfigClientCommand, DecryptCommand, EncryptCommand
from config.spring import ConfigClient
from tests import conftest

application = Application()
application.add(ConfigClientCommand())
application.add(DecryptCommand())
application.add(EncryptCommand())


SAMPLE_CONFIG = {"db": {"user": "root", "pass": "123"}}


class TestClientCommand:
    def get_config_mock(self, *args, **kwargs):
        return SAMPLE_CONFIG

    @pytest.fixture
    def command(self):
        command = application.find("client")
        return CommandTester(command)

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

    def test_show_all_config(self, command, config_mock):
        command.execute("app --all")
        assert command.io.fetch_output() is not None

    def test_show_filter_config(self, command, attribute_mock):
        command.execute("app db -v")
        assert command.io.fetch_output() is not None

    def test_connection_error(self, command, monkeypatch):
        monkeypatch.setattr(http, "get", SystemExit())
        with pytest.raises(SystemExit):
            command.execute("app --all")

    def test_empty_response(self, command, monkeypatch):
        monkeypatch.setattr(ConfigClient, "get_config", self.dumb_func)
        with pytest.raises(SystemExit):
            command.execute("app")

    def test_save_as_json(self, command, attribute_mock):
        command.execute("app db --json")
        assert command.io.fetch_output() is not None

    def test_custom_url_via_env(self, command, monkeypatch):
        monkeypatch.setenv("CONFIGSERVER_CUSTOM_URL", "http://localhost")
        monkeypatch.setattr(ConfigClient, "get_config", self.dumb_func)
        with pytest.raises(SystemExit):
            command.execute("app 'db' --json")

    def test_get_file(self, command, monkeypatch):
        monkeypatch.setattr(http, "get", conftest.text_mock)
        with pytest.raises(SystemExit):
            command.execute("app nginx.conf --file")

    def test_get_file_error(self, command, monkeypatch):
        monkeypatch.setattr(http, "get", SystemExit())
        with pytest.raises(SystemExit):
            command.execute("app nginx.conf --file")

    @pytest.mark.parametrize(
        "cmdline", ["app --all --auth user:pass", "app --all --digest user:pass"]
    )
    def test_get_config(self, command, monkeypatch, cmdline, config_mock):
        command.execute(cmdline)
        assert command.io.fetch_output() is not None

    @pytest.mark.parametrize(
        "cmdline,error",
        [
            ("app --all --auth user:pass", conftest.connection_error),
            ("app --all --auth user:pass", conftest.value_error),
            ("app --all --digest user:pass", conftest.connection_error),
            ("app --all --digest user:pass", conftest.value_error),
        ],
    )
    def test_get_config_with_auth_error(self, command, monkeypatch, cmdline, error):
        monkeypatch.setattr(ConfigClient, "get_config", error)
        with pytest.raises(SystemExit):
            command.execute(cmdline)


class TestDecryptCommand:
    def _mock_decrypt(self, *args, **kwargs):
        return "my-secret"

    def test_decrypt_command(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "decrypt", self._mock_decrypt)
        command = application.find("decrypt")
        ct = CommandTester(command)
        ct.execute(conftest.ENCRYPTED_DATA)
        assert ct.io.fetch_output() is not None

    def test_decrypt_command_error(self, monkeypatch):
        monkeypatch.setattr(http, "post", SystemExit())
        with pytest.raises(SystemExit):
            command = application.find("decrypt")
            ct = CommandTester(command)
            ct.execute(conftest.ENCRYPTED_DATA)


class TestEncryptCommand:
    def _mock_encrypt(self, *args, **kwargs):
        return f"{{cipher}}{conftest.ENCRYPTED_DATA}"

    def _mock_encrypt_raw(self, *args, **kwargs):
        return conftest.ENCRYPTED_DATA

    def test_encrypt_command(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "encrypt", self._mock_encrypt)
        command = application.find("encrypt")
        ct = CommandTester(command)
        ct.execute("my-secret")
        assert ct.io.fetch_output() is not None

    def test_encrypt_command_raw(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "encrypt", self._mock_encrypt_raw)
        command = application.find("encrypt")
        ct = CommandTester(command)
        ct.execute("my-secret --raw")
        assert ct.io.fetch_output() is not None

    def test_encrypt_command_error(self, monkeypatch):
        monkeypatch.setattr(http, "post", SystemExit())
        with pytest.raises(SystemExit):
            command = application.find("encrypt")
            ct = CommandTester(command)
            ct.execute("my-secret")
