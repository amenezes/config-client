import json
import random
import sys
from typing import List

import yaml
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
        {--yaml : Save output as yaml.}
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
        )
        self.line("\U000023f3 contacting server...")

        client.get_config()
        emoji = random.choice(self.EMOJI_ERRORS)
        self.line(f"{emoji} failed to contact server... {emoji}")
        emoji = random.choice(self.EMOJI_SUCCESS)
        self.line(f"{emoji} Ok! {emoji}")

        if self.option("all"):
            output = client.config
        else:
            output = client.get_attribute(f"{filter_options}")

        if len(output) == 0:
            emoji = random.choice(self.EMOJI_NOT_FOUND)
            self.line(
                f"{emoji} no result found for your filter: <comment>'{filter_options}'<comment>"
            )
            sys.exit(0)

        if self.option("json"):
            self.file_output("json", json.dumps(output))
        elif self.option("yaml"):
            self.file_output("yaml", yaml.dump(output))
        else:
            self.table_output(filter_options, output)

    def table_output(self, filter_options: str, content: str) -> None:
        if self.option("all"):
            filter_options = "all"
        headers = [
            f"<options=bold>report for filter: <comment>'{filter_options}'</comment></>"
        ]
        rows = [[f"{content}"]]
        table = self.table(header=headers, rows=rows, style="solid")
        table.render(self.io)

    def file_output(self, file_format, content):
        self.line(f"generating <info>{file_format}</info> file...")
        self.save_to_file(f"output.{file_format}", content)
        self.line(f"file saved: <info>output.{file_format}</info>")

    def save_to_file(self, filename: str, content: str):
        with open(filename, "w") as f:
            f.write(content)
