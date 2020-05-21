import logging

from .__version__ import __version__

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
