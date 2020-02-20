import pytest
import requests
from cleo import Application, CommandTester

from config.cli import CloudFoundryCommand, ConfigClientCommand
from config.spring import ConfigClient

application = Application()
application.add(CloudFoundryCommand())
application.add(ConfigClientCommand())


SAMPLE_CONFIG = {"db": {"user": "root", "pass": "123"}}


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

    @pytest.fixture
    def connection_mock(self, monkeypatch):
        monkeypatch.setattr(ConfigClient, "get_config", print)

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
        monkeypatch.setattr(requests, "get", SystemExit)
        with pytest.raises(SystemExit):
            command.execute("app --all")

    def test_empty_response(self, command, monkeypatch):
        monkeypatch.setattr(ConfigClient, "get_config", print)
        with pytest.raises(SystemExit):
            command.execute("app")

    def test_save_as_json(self, command, attribute_mock):
        command.execute("app 'db' --json")
        assert "generating json file" in command.io.fetch_output()

    def test_custom_url_via_env(self, command, monkeypatch):
        monkeypatch.setenv("CONFIGSERVER_CUSTOM_URL", "http://localhost")
        monkeypatch.setattr(ConfigClient, "get_config", print)
        with pytest.raises(SystemExit):
            command.execute("app 'db' --json")
