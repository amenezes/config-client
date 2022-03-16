import json
import logging
import os
import random
import re
from typing import Any, List

from cleo import Command
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.status import Status
from rich.table import Table

from config.exceptions import RequestFailedException
from config.spring import ConfigClient

logging.disable(logging.ERROR)
console = Console()


class ConfigClientCommand(Command):
    """
    Interact with Spring Cloud Server via cli.

    client
        {app : Application name.}
        {filter? : Config selector.}
        {--a|address=http://localhost:8888 : ConfigServer address.}
        {--l|label=master : Branch config.}
        {--p|profile=development : Profile config.}
        {--file : Gets remote file from server and saves locally.}
        {--json : Save output as json.}
        {--all : Show all config.}
        {--auth= : Basic authentication credentials.}
        {--digest= : Digest authentication credentials.}
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
        client = ConfigClient(
            address=os.getenv("CONFIGSERVER_ADDRESS", self.option("address")),
            label=os.getenv("LABEL", self.option("label")),
            app_name=os.getenv("APP_NAME", self.argument("app")),
            profile=os.getenv("PROFILE", self.option("profile")),
            fail_fast=False,
        )

        if self.option("file"):
            self.request_file(client, filter_options)
            raise SystemExit(0)

        content = self.request_config(client, filter_options)
        if self.option("json"):
            self.save_json("output.json", content)
        else:
            self.std_output(filter_options, content)

    def request_config(self, client: ConfigClient, filter_options: str) -> Any:
        if self.io.verbosity:
            table = Table.grid(padding=(0, 1))
            table.add_column(style="cyan", justify="right")
            table.add_column(style="magenta")

            table.add_row("address[yellow]:[/yellow] ", client.address)
            table.add_row("label[yellow]:[/yellow] ", client.label)
            table.add_row("profile[yellow]:[/yellow] ", client.profile)
            table.add_row("URL[yellow]:[/yellow] ", client.url)
            console.print(
                Panel(
                    table,
                    title="[bold yellow]client info[/bold yellow]",
                    border_style="yellow",
                    expand=True,
                )
            )

        with Status("contacting server...", spinner="dots4") as status:
            emoji = random.choice(self.EMOJI_ERRORS)
            try:
                if self.option("auth"):
                    username, password = self.option("auth").split(":")
                    auth = HTTPBasicAuth(username, password)
                elif self.option("digest"):
                    username, password = self.option("digest").split(":")
                    auth = HTTPDigestAuth(username, password)  # type: ignore
                else:
                    auth = None
                client.get_config(auth=auth)
            except ValueError:
                console.print(
                    f"\nbad credentials format for auth method. Format expected: user:password {emoji}",
                    style="bold",
                )
                raise SystemExit(1)
            except ConnectionError:
                console.print(
                    f"\n[red]failed to contact server![/red] {emoji}", style="bold"
                )
                raise SystemExit(1)

            status.update("OK!")
        content = self.get_config(client, filter_options)
        self.has_content(content, filter_options)
        return content

    def request_file(self, client: ConfigClient, filter_options: str) -> None:
        with Status("contacting server...", spinner="dots4") as status:
            try:
                response = client.get_file(filter_options)
            except RequestFailedException:
                emoji = random.choice(self.EMOJI_ERRORS)
                console.print(
                    f"\n[red]failed to contact server![/red] {emoji}", style="bold"
                )
                raise SystemExit(1)
            with open(f"{filter_options}", "w", encoding="utf-8") as f:
                f.write(response)
            status.update("OK!")
        console.print(f"file saved: [cyan]{filter_options}[/cyan]", style="bold")

    def get_config(self, client: ConfigClient, filter_options: str) -> Any:
        if self.option("all"):
            content = client.config
        else:
            content = client.get(f"{filter_options}")
        return content

    def has_content(self, content, filter_options: str) -> None:
        if len(str(content)) == 0:
            emoji = random.choice(self.EMOJI_NOT_FOUND)
            console.print(
                f"\n{emoji} no result found for filter: [yellow]'[white bold]{filter_options}[/white bold]'[/yellow]",
            )
            raise SystemExit(0)

    def std_output(self, filter_options: str, content: str) -> None:
        if self.option("all"):
            filter_options = "all"
        console.print(
            Panel(
                JSON(json.dumps(content), indent=4, highlight=True, sort_keys=True),
                title=f"[bold green]report for filter: [yellow]'[white italic]{filter_options}[/white italic]'[/yellow][/bold green]",
                highlight=True,
                border_style="white",
                expand=True,
            )
        )

    def save_json(self, filename: str, content: str) -> None:
        with open(f"{filename}", "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4, sort_keys=True)
        console.print(f"file saved: [cyan]{filename}[/cyan]", style="bold")


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
            console.print("\n[red]failed to contact server![/red]", style="bold")
            raise SystemExit(1)
        console.print(f"[cyan]{resp}[/cyan]")


class EncryptCommand(Command):
    """
    Encrypt a input via Spring Cloud Config.

    encrypt
        {data : Data to encrypt.}
        {--a|address=http://localhost:8888 : ConfigServer address.}
        {--p|path=/encrypt : encrypt path.}
        {--raw : Format output including {cipher}?}
    """

    def handle(self):
        client = ConfigClient(
            address=os.getenv("CONFIGSERVER_ADDRESS", self.option("address")),
            fail_fast=False,
        )
        try:
            resp = client.encrypt(self.argument("data"), path=self.option("path"))
        except Exception:
            console.print("[red]failed to contact server![/red]", style="bold")
            raise SystemExit(1)
        if not self.option("raw"):
            console.print(
                f"[yellow]'[white]{{cipher}}{resp}[/white]'[/yellow]",
                style="bold",
            )
        else:
            console.print(resp)
