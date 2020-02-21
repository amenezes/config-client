from typing import Any

import attr
from flask.app import Flask
from flask.config import Config
from glom import glom

from config.spring import ConfigClient


def _validate(instance, attribute, value) -> None:
    client = instance._client
    if client.__class__.__name__ not in ("ConfigClient", "CF"):
        raise TypeError(f"instance must be <ConfigClient> or <CF> (got: {client})")


@attr.s(frozen=True)
class FlaskConfig:
    app = attr.ib(type=Flask, validator=attr.validators.instance_of(Flask), repr=False)
    _client = attr.ib(factory=ConfigClient, validator=_validate)

    def __attrs_post_init__(self) -> None:
        self._client.get_config()
        self.app.config = _Config(
            root_path=self.app.root_path,
            defaults=self.app.config,
            _config=self._client.config,
        )


class _Config(Config):
    def __init__(self, _config, *args, **kwargs):
        super(_Config, self).__init__(*args, **kwargs)
        Config.update(self, _config)

    def get(self, key, default=None) -> Any:
        return glom(self, key, default=default)
