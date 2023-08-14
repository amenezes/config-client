from fastapi import Request

from config import CF, ConfigClient
from config.logger import logger


async def fastapi_config_client(request: Request):
    """Configure FastAPI application with config-client.

    Usage:

    from fastapi import Depends, FastAPI
    from config.ext.fastapi import fastapi_config_client


    app = FastAPI(dependencies=[Depends(fastapi_config_client)])

    @app.get("/info")
    def consul(request: Request):
    return dict(
        description=request.app.config_client.get("info.app.description"),
        url=request.app.config_client.get("info.app.name"),
    )
    """
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
    """Configure FastAPI application with config-client.

    Usage:

    from fastapi import Depends, FastAPI
    from config.ext.fastapi import fastapi_cloud_foundry


    app = FastAPI(dependencies=[Depends(fastapi_cloud_foundry)])

    @app.get("/info")
    def consul(request: Request):
    return dict(
        description=request.app.config_client.get("info.app.description"),
        url=request.app.config_client.get("info.app.name"),
    )
    """
    try:
        logger.debug("ConfigClient already initialized")
    except AttributeError:
        logger.debug("Initializing ConfigClient")
        cc = CF()
        cc.get_config()
        request.app.config_client = cc
        logger.debug("ConfigClient successfully initialized")
