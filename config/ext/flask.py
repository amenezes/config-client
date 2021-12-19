from typing import Any, Optional

from flask.app import Flask
from flask.config import Config
from glom import glom

from config.logger import logger
from config.spring import ConfigClient


def _validate(instance) -> None:
    instance_type = instance.__class__.__name__
    if instance_type not in ("ConfigClient", "CF"):
        raise TypeError(
            f"instance must be <ConfigClient> or <CF> (got: {instance_type})"
        )


class FlaskConfig:
    def __init__(
        self, app: Flask, client: Optional[ConfigClient] = None, **kwargs
    ) -> None:
        if not isinstance(app, Flask):
            raise TypeError("app must be Flask instance")

        if not client:
            client = ConfigClient()
        _validate(client)

        self.app = app
        logger.debug(f"FlaskConfig get_config params: [kwargs='{kwargs}']")
        client.get_config(**kwargs)
        self.app.config = _Config(
            root_path=self.app.root_path,
            defaults=self.app.config,
            _config=client.config,
        )


class _Config(Config):
    def __init__(self, _config, *args, **kwargs):
        super(_Config, self).__init__(*args, **kwargs)
        Config.update(self, _config)

    def get(self, key, default: Any = None) -> Any:
        return glom(self, key, default=default)
