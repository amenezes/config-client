from aiohttp import web
from glom import glom

from config.spring import ConfigClient


class AioHttpConfig:
    def __init__(
        self, app: web.Application, key: str = "config", client=ConfigClient()
    ) -> None:
        self._validate_app(app)
        self._validate_client(client)
        client.get_config()
        app[str(key)] = _Config(client.config)

    def _validate_app(self, app: web.Application) -> None:
        if not isinstance(app, web.Application):
            raise TypeError("instance must be <aiohttp.web.Application>")

    def _validate_client(self, client) -> None:
        if client.__class__.__name__ not in ("ConfigClient", "CF"):
            raise TypeError("instance must be <ConfigClient> or <CF>")


class _Config(dict):
    def get(self, key, default=None):
        return glom(self, key, default=default)
