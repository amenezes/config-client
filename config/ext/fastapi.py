from fastapi import Request

from config import CF, ConfigClient
from config.logger import logger


async def fastapi_config_client(request: Request):
    try:
        request.app.config_client
        logger.debug("ConfigClient already initialized")
    except AttributeError:
        logger.debug("Initializing ConfigClient")
        cc = ConfigClient()
        cc.get_config()
        request.app.config_client = cc
        logger.debug("ConfigClient successfully initialized")


async def fastapi_cloud_foundry(request: Request):
    try:
        logger.debug("ConfigClient already initialized")
    except AttributeError:
        logger.debug("Initializing ConfigClient")
        cc = CF()
        cc.get_config()
        request.app.config_client = cc
        logger.debug("ConfigClient successfully initialized")
