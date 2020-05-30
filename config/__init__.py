import logging

from .__version__ import __version__

logger = logging.getLogger("config-client")
logger.addHandler(logging.NullHandler())
