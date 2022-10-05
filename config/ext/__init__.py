try:
    from config.ext.aiohttp import AioHttpConfig
except ImportError:
    aiohttp = None

try:
    from config.ext.flask import FlaskConfig
except ImportError:
    flask = None


try:
    from config.ext.fastapi import fastapi_cloud_foundry, fastapi_config_client
except ImportError:
    fastapi = None


__all__ = [
    "AioHttpConfig",
    "FlaskConfig",
    "fastapi_config_client,",
    "fastapi_cloud_foundry",
]
