import json
import random
from typing import List

from cleo import Command

from config.spring import ConfigClient


class CloudFoundryCommand(Command):
    """
    Interact with CloudFoundry via cli.

    cf
    """

    def handle(self):
        pass


class ConfigClientCommand(Command):
    """
    Interact with Spring Cloud Server via cli.

    client
        {app : Application name.}
        {filter? : Config selector.}
        {--a|address=http://localhost:8888 : ConfigServer address.}
        {--b|branch=master : Branch config.}
        {--p|profile=development : Profile config.}
        {--u|url : Base URL format. <option=bold>(default: "<address>/<branch>/<app>-<profile>")</>}
        {--json : Save output as json}
        {--all : Show all config.}
    """

    EMOJI_ERRORS: List[str] = [
        "\U0001f92f",
        "\U0001f635",
        "\U0001f92e",
        "\U0001f922",
        "\U0001f628",
        "\U0001f62d",
        "\U0001f4a9",
        "\U0001f494",
        "\U0001f4a5",
        "\U0001f525",
    ]
    EMOJI_SUCCESS: List[str] = [
        "\U0001f973",
        "\U0001f929",
        "\U0001f63b",
        "\U0001f496",
        "\U0001f389",
        "\U0001f38a",
    ]
    EMOJI_NOT_FOUND = [
        "\U0001f642",
        "\U0001f60c",
        "\U0001f928",
        "\U0001f643",
        "\U0001f605",
    ]

    def handle(self):
        url = f"{self.option('address')}/{self.option('branch')}/{self.argument('app')}-{self.option('profile')}.json"
        filter_options = self.argument("filter") or ""

        client = ConfigClient(
            address=self.option("address") or "http://localhost:8888",
            branch=self.option("branch") or "master",
            app_name=self.argument("app") or "",
            profile=self.option("profile") or "development",
            url=self.option("url") or url,
            fail_fast=False,
        )

        content = self.request_config(client, filter_options)

        if self.option("json"):
            self.save_file("output.json", json.dumps(content))
        else:
            self.table_output(filter_options, content)

    def request_config(self, client: ConfigClient, filter_options: str):
        self.line("\U000023f3 contacting server...")
        try:
            client.get_config()
        except ConnectionError:
            emoji = random.choice(self.EMOJI_ERRORS)
            self.line(f"{emoji} failed to contact server... {emoji}")
            raise SystemExit(1)

        self.print_contact_server_ok()
        content = self.get_config(client, filter_options)
        self.has_content(content, filter_options)
        return content

    def get_config(self, client, filter_options):
        if self.option("all"):
            content = client.config
        else:
            content = client.get_attribute(f"{filter_options}")
        return content

    def print_contact_server_ok(self):
        emoji = random.choice(self.EMOJI_SUCCESS)
        self.line(f"{emoji} Ok! {emoji}")

    def has_content(self, content, filter_options) -> None:
        if len(content) == 0:
            emoji = random.choice(self.EMOJI_NOT_FOUND)
            self.line(
                f"{emoji} no result found for your filter: <comment>'{filter_options}'<comment>"
            )
            raise SystemExit(0)

    def table_output(self, filter_options: str, content: str) -> None:
        if self.option("all"):
            filter_options = "all"
        headers = [
            f"<options=bold>report for filter: <comment>'{filter_options}'</comment></>"
        ]
        rows = [[f"{content}"]]
        table = self.table(header=headers, rows=rows, style="solid")
        table.render(self.io)

    def save_file(self, filename: str, content: str):
        extension = filename[-4:]
        self.line(f"generating <info>{extension}</info> file...")
        with open(f"{filename}", "w") as f:
            f.write(content)
        self.line(f"file saved: <info>{filename}</info>")
