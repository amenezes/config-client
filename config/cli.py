import random
import re
from json import dump, dumps
from pathlib import Path
from typing import List

import click
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.status import Status
from rich.table import Table

from config import __version__
from config.exceptions import RequestFailedException
from config.spring import ConfigClient

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)
EMOJI_ERRORS: List[str] = ["🤯", "😵", "🤮", "🤢", "😨", "😭", "💩", "💔", "💥", "🔥"]
EMOJI_SUCCESS: List[str] = ["🥳", "🤩", "😻", "💖", "🎉", "🎊"]
EMOJI_NOT_FOUND = ["🙂", "😌", "🤨", "🙃", "😅"]

console = Console()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.argument("app_name", envvar="APP_NAME")
@click.option(
    "-a",
    "--address",
    envvar="CONFIGSERVER_ADDRESS",
    required=True,
    default="http://localhost:8888",
    show_default=True,
    help="ConfigServer address.",
)
@click.option(
    "-l",
    "--label",
    envvar="LABEL",
    required=True,
    default="master",
    show_default=True,
    help="Branch config.",
)
@click.option(
    "-p",
    "--profile",
    envvar="PROFILE",
    required=True,
    default="development",
    show_default=True,
    help="Profile config.",
)
@click.option("-f", "--filter", required=False, help="Filter output by.")
@click.option("--auth", required=False, help="Basic authentication credentials.")
@click.option("--digest", required=False, help="Digest authentication credentials.")
@click.option(
    "--file", required=False, help="Gets remote file from server and saves locally."
)
@click.option("--json", is_flag=True, required=False, help="Save output as json.")
@click.option("-v", "--verbose", is_flag=True, help="Extend output info.")
def client(
    app_name, address, label, profile, filter, auth, digest, file, json, verbose
):
    """Interact with Spring Cloud Server via cli."""
    client = ConfigClient(
        address=address,
        label=label,
        app_name=app_name,
        profile=profile,
        fail_fast=False,
    )

    if file:
        # get file from server and exit
        with Status("Contacting server...", spinner="dots4") as status:
            try:
                resp = client.get_file(file)
            except RequestFailedException:
                raise click.ClickException("💥 Failed to contact server!")
            Path(file).write_text(resp)
            status.update("OK!")
        console.print(f"File saved: [cyan]{file}[/cyan]", style="bold")
        raise SystemExit

    if verbose:
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

    with Status("Contacting server...", spinner="dots4") as status:
        emoji = random.choice(EMOJI_ERRORS)
        try:
            if auth:
                username, password = auth.split(":")
                auth = HTTPBasicAuth(username, password)
            elif digest:
                username, password = digest.split(":")
                auth = HTTPDigestAuth(username, password)
            else:
                auth = None
            client.get_config(auth=auth)
        except ValueError:
            raise click.ClickException(
                f"{emoji} Bad credentials format for auth method. Format expected: <user>:<password>"
            )
        except ConnectionError:
            raise click.ClickException("💥 Failed to contact server!")
        status.update("OK!")

        content = client.config
        if filter:
            content = client.get(filter)

    if len(str(content)) == 0:
        emoji = random.choice(EMOJI_NOT_FOUND)
        console.print(
            f"{emoji} No result found for filter: [yellow]'[white bold]{filter}[/white bold]'[/yellow]",
        )
        raise SystemExit

    if json:
        with open("response.json", "w", encoding="utf-8") as f:
            dump(content, f, indent=4, sort_keys=True)
        console.print("File saved: [cyan]response.json[/cyan]", style="bold")
        raise SystemExit

    filter = filter or "all"
    console.print(
        Panel(
            JSON(dumps(content), indent=4, highlight=True, sort_keys=True),
            title=f"[bold][green]report for filter[/green][yellow]: [/yellow]'[magenta italic]{filter}[/magenta italic]'[/bold]",
            highlight=True,
            border_style="white",
            expand=True,
        )
    )


@cli.command()
@click.argument("text")
@click.option(
    "-a",
    "--address",
    envvar="CONFIGSERVER_ADDRESS",
    required=True,
    default="http://localhost:8888",
    help="ConfigServer address.",
)
@click.option(
    "-p", "--path", required=True, default="/decrypt", help="Decrypt path endpoint."
)
def decrypt(text, address, path):
    """Decrypt a input via Spring Cloud Config."""
    client = ConfigClient(address=address, fail_fast=False)
    cipher = re.match(r"^.?{cipher}?(?P<name>\w.*)", text)
    if cipher:
        text = cipher.group("name")

    try:
        resp = client.decrypt(text, path=path)
    except Exception:
        raise click.ClickException("💥 Failed to contact server!")

    table = Table.grid(padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("decrypted data[yellow]:[/yellow] ", f"'{resp}'")
    console.print(Panel(table, border_style="yellow", expand=True))


@cli.command()
@click.argument("data")
@click.option(
    "-a",
    "--address",
    envvar="CONFIGSERVER_ADDRESS",
    default="http://localhost:8888",
    required=True,
    help="ConfigServer address.",
)
@click.option(
    "-p", "--path", default="/encrypt", required=True, help="Encrypt path endpoint."
)
@click.option("--raw", is_flag=True, help=r"Format output including {cipher}")
def encrypt(data, address, path, raw):
    """Encrypt a input via Spring Cloud Config."""
    client = ConfigClient(address=address, fail_fast=False)
    try:
        resp = client.encrypt(data, path=path)
    except Exception:
        raise click.ClickException("💥 Failed to contact server!")

    if raw:
        resp = f"{{cipher}}{resp}"

    table = Table.grid(padding=(0, 1))
    table.add_column(style="cyan", justify="right")
    table.add_column(style="magenta")

    table.add_row("encrypted data[yellow]:[/yellow] ", f"'{resp}'")
    console.print(Panel(table, border_style="yellow", expand=True))
