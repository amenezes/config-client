from typing import Any, Optional

from aiohttp import web
from glom import glom

from config.logger import logger
from config.spring import ConfigClient


class AioHttpConfig:
    def __init__(
        self,
        app: web.Application,
        key: str = "config",
        client: Optional[ConfigClient] = None,
        **kwargs,
    ) -> None:
        self._validate_app(app)
        if not client:
            client = ConfigClient()
        self._validate_client(client)
        logger.debug(f"AioHttpConfig get_config params: [kwargs='{kwargs}']")
        client.get_config(**kwargs)
        app[str(key)] = _Config(client.config)

    def _validate_app(self, app: web.Application) -> None:
        if not isinstance(app, web.Application):
            raise TypeError("instance must be <aiohttp.web.Application>")

    def _validate_client(self, client) -> None:
        if client.__class__.__name__ not in ("ConfigClient", "CF"):
            raise TypeError("instance must be <ConfigClient> or <CF>")


class _Config(dict):
    def get(self, key, default: Any = None) -> Any:
        return glom(self, key, default=default)
