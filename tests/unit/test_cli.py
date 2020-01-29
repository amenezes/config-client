import pytest
from cleo import Application, CommandTester

from config.cli import CloudFoundryCommand, ConfigClientCommand
from config.spring import ConfigClient

application = Application()
application.add(CloudFoundryCommand())
application.add(ConfigClientCommand())


class TestCloudFoundryCommand:
    def test_cf_command(self):
        command = application.find("cf")
        ct = CommandTester(command)
        ct.execute("-h")
        assert "" == ct.io.fetch_output()


class TestClientCommand:
    @pytest.fixture
    def client(self, mocker):
        c = mocker.patch.object(
            ConfigClient,
            "get_config",
            return_value={"db": {"user": "user", "pass": "pass"}},
        )
        return c

    @pytest.mark.skip
    def test_client_command(self, client):
        command = application.find("client")
        ct = CommandTester(command)
        ct.execute("app 'db'")
        assert "\U0001f4c4" == ct.io.fetch_output()

    def test_client_command_empty_result(self, client):
        command = application.find("client")
        ct = CommandTester(command)
        with pytest.raises(SystemExit):
            ct.execute("app ''")

    def test_show_all(self):
        pass

    def test_client_output_json(self):
        pass

    def test_client_output_yaml(self):
        pass
