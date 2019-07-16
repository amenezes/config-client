"""Core functions."""
from functools import wraps


def singleton(cls):
    """Ensure singleton instance."""
    instances = {}

    @wraps(cls)
    def instance(*args, **kwargs):
        """Create class instance."""
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return instance
