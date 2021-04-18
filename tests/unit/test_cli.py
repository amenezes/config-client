import pytest
from cleo import Application, CommandTester

from config import http
from config.cli import (
    CloudFoundryCommand,
    ConfigClientCommand,
    DecryptCommand,
    EncryptCommand,
)
from config.spring import ConfigClient
from tests import conftest

application = Application()
application.add(CloudFoundryCommand())
application.add(ConfigClientCommand())
application.add(DecryptCommand())
application.add(EncryptCommand())


SAMPLE_CONFIG = {"db": {"user": "root", "pass": "123"}}
DATA = "my-secret"
ENCRYPTED_DATA = "AQC4HPhv2tHW3irTDlFUQ7nBEuPiRiK/RNp0JOHfoS0MrgOxqUAYYnKo5YEu+lDOVm+8EKeRhuw8o+rPmSxDCiNZ7FrriFRAde4ZTJ45FTVzW6COFFEkuXJQktZ2dCqGKLeRrTwWQ98g0X7ee9nEsQXK40yKQRhPCXPFgLY9J0BEukn8i1omFtxSFJ0MGILt5n/Sen9/MOGp+yJXGw7FMLejBpVMc4m9rFDyTskyk8OiobbFfG/osAaNRc2R/cTDEHAXVJVw9QwMWp3EJKpOwnx1YVmL3+4msGLYtRpB0XSrGo2AbUNa+5xTwdXIehmIAbn/TckOJE4sBc6vTSjxmtkNcE9cLDC+nlH0ANR9r/9uPqNFErXWrUlbEMJQ9SU4XdU="


class TestCloudFoundryCommand:
    def test_cf_command(self):
        command = application.find("cf")
        ct = CommandTester(command)
        ct.execute("-h")
        assert "" == ct.io.fetch_output()


class TestClientCommand:
    def get_attribute_mock(self, *args, **kwargs):
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
        monkeypatch.setattr(ConfigClient, "get_attribute", self.get_attribute_mock)

    def test_show_all_config(self, command, config_mock):
        command.execute("app --all")
        assert "report for filter: 'all'" in command.io.fetch_output()

    def test_show_filter_config(self, command, attribute_mock):
        command.execute("app 'db'")
        assert "report for filter: 'db'" in command.io.fetch_output()

    def test_connection_error(self, command, monkeypatch):
        monkeypatch.setattr(http, "get", SystemExit())
        with pytest.raises(SystemExit):
            command.execute("app --all")

    def test_empty_response(self, command, monkeypatch):
        monkeypatch.setattr(ConfigClient, "get_config", self.dumb_func)
        with pytest.raises(SystemExit):
            command.execute("app")

    def test_save_as_json(self, command, attribute_mock):
        command.execute("app 'db' --json")
        assert "generating json file" in command.io.fetch_output()

    def test_custom_url_via_env(self, command, monkeypatch):
        monkeypatch.setenv("CONFIGSERVER_CUSTOM_URL", "http://localhost")
        monkeypatch.setattr(ConfigClient, "get_config", self.dumb_func)
        with pytest.raises(SystemExit):
            command.execute("app 'db' --json")

    def test_get_file(self, command, monkeypatch):
        monkeypatch.setattr(http, "get", conftest.response_mock_success)
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
        assert "report for filter: 'all'" in command.io.fetch_output()

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
        return DATA

    def test_decrypt_command(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "decrypt", self._mock_decrypt)
        command = application.find("decrypt")
        ct = CommandTester(command)
        ct.execute(ENCRYPTED_DATA)
        assert DATA in ct.io.fetch_output()

    def test_decrypt_command_error(self, monkeypatch):
        monkeypatch.setattr(http, "post", SystemExit())
        with pytest.raises(SystemExit):
            command = application.find("decrypt")
            ct = CommandTester(command)
            ct.execute(ENCRYPTED_DATA)


class TestEncryptCommand:
    def _mock_encrypt(self, *args, **kwargs):
        return f"{{cipher}}{ENCRYPTED_DATA}"

    def _mock_encrypt_raw(self, *args, **kwargs):
        return ENCRYPTED_DATA

    def test_encrypt_command(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "encrypt", self._mock_encrypt)
        command = application.find("encrypt")
        ct = CommandTester(command)
        ct.execute(DATA)
        assert ENCRYPTED_DATA in ct.io.fetch_output()

    def test_encrypt_command_raw(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "encrypt", self._mock_encrypt_raw)
        command = application.find("encrypt")
        ct = CommandTester(command)
        ct.execute(f"{DATA} --raw=yes")
        assert ENCRYPTED_DATA in ct.io.fetch_output()

    def test_encrypt_command_error(self, monkeypatch):
        monkeypatch.setattr(http, "post", SystemExit())
        with pytest.raises(SystemExit):
            command = application.find("encrypt")
            ct = CommandTester(command)
            ct.execute(DATA)
