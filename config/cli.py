import json
import logging
import os
import random
import re
from pathlib import Path
from typing import Any, List

from cleo import Command
from dotenv import load_dotenv

from config.exceptions import RequestFailedException
from config.spring import ConfigClient

logging.disable(logging.ERROR)


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


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
        {--file : Gets remote file from server and saves locally.}
        {--json : Save output as json.}
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

    def handle(self) -> None:
        filter_options = self.argument("filter") or ""
        host = os.getenv("CONFIGSERVER_ADDRESS", self.option("address"))
        url = os.getenv("CONFIGSERVER_CUSTOM_URL")
        if not url:
            url = f"{host}/{self.option('branch')}/{self.argument('app')}-{self.option('profile')}.json"

        client = ConfigClient(
            address=os.getenv("CONFIGSERVER_ADDRESS", self.option("address")),
            branch=os.getenv("BRANCH", self.option("branch")),
            app_name=os.getenv("APP_NAME", self.argument("app")),
            profile=os.getenv("PROFILE", self.option("profile")),
            url=self.option("url") or url,
            fail_fast=False,
        )

        if self.option("file"):
            self.request_file(client, filter_options)
            raise SystemExit(0)

        content = self.request_config(client, filter_options)
        if self.option("json"):
            self.save_file("output.json", content)
        else:
            self.std_output(filter_options, content)

    def request_config(self, client: ConfigClient, filter_options: str) -> Any:
        self.line("<options=bold>\U000023f3 contacting server...</>")
        try:
            client.get_config()
        except ConnectionError:
            emoji = random.choice(self.EMOJI_ERRORS)
            self.line(f"<options=bold>{emoji} failed to contact server... {emoji}</>")
            raise SystemExit(1)

        self.print_contact_server_ok()
        content = self.get_config(client, filter_options)
        self.has_content(content, filter_options)
        return content

    def request_file(self, client: ConfigClient, filter_options: str) -> None:
        self.line("<options=bold>\U000023f3 contacting server...</>")
        try:
            response = client.get_file(filter_options)
        except RequestFailedException:
            emoji = random.choice(self.EMOJI_ERRORS)
            self.line(f"<options=bold>{emoji} failed to contact server... {emoji}</>")
            raise SystemExit(1)
        with open(f"{filter_options}", "w") as f:
            f.write(response)
        self.line(f"file saved: <info>{filter_options}</info>")

    def get_config(self, client: ConfigClient, filter_options: str) -> Any:
        if self.option("all"):
            content = client.config
        else:
            content = client.get_attribute(f"{filter_options}")
        return content

    def print_contact_server_ok(self) -> None:
        emoji = random.choice(self.EMOJI_SUCCESS)
        self.line(f"<options=bold>{emoji} Ok! {emoji}</>")

    def has_content(self, content, filter_options: str) -> None:
        if len(str(content)) == 0:
            emoji = random.choice(self.EMOJI_NOT_FOUND)
            self.line(
                f"{emoji} no result found for your filter: <comment>'{filter_options}'</comment>"
            )
            raise SystemExit(0)

    def std_output(self, filter_options: str, content: str) -> None:
        if self.option("all"):
            filter_options = "all"
        self.line(
            f"<options=bold>\U0001f4c4 report for filter: <comment>'{filter_options}'</comment>:</>"
        )
        self.line(f"{json.dumps(content, indent=4, sort_keys=True)}")

    def save_file(self, filename: str, content: str) -> None:
        extension = filename[-4:]
        self.line(f"generating <info>{extension}</info> file...")
        with open(f"{filename}", "w") as f:
            json.dump(content, f, indent=4, sort_keys=True)
        self.line(f"file saved: <info>{filename}</info>")


class DecryptCommand(Command):
    """
    Decrypt a input via Spring Cloud Config.

    decrypt
        {data : Data to decrypt.}
        {--a|address=http://localhost:8888 : ConfigServer address.}
        {--p|path=/decrypt : decrypt path.}
    """

    def handle(self):
        client = ConfigClient(
            address=os.getenv("CONFIGSERVER_ADDRESS", self.option("address")),
            fail_fast=False,
        )
        try:
            data = re.match(r"^.?{cipher}?(?P<name>\w.*)", self.argument("data")).group(
                "name"
            )
        except AttributeError:
            data = self.argument("data")
        try:
            resp = client.decrypt(data, path=self.option("path"))
        except Exception:
            self.line("<options=bold>failed to contact server... </>")
            raise SystemExit(1)
        self.line(resp)


class EncryptCommand(Command):
    """
    Encrypt a input via Spring Cloud Config.

    encrypt
        {data : Data to encrypt.}
        {--a|address=http://localhost:8888 : ConfigServer address.}
        {--p|path=/encrypt : encrypt path.}
        {--raw=no : Format output including {cipher}?}
    """

    def handle(self):
        client = ConfigClient(
            address=os.getenv("CONFIGSERVER_ADDRESS", self.option("address")),
            fail_fast=False,
        )
        try:
            resp = client.encrypt(self.argument("data"), path=self.option("path"))
        except Exception:
            self.line("<options=bold>failed to contact server... </>")
            raise SystemExit(1)
        if not self.option("raw") == "yes":
            self.line(f"'{{cipher}}{resp}'")
        else:
            self.line(resp)
