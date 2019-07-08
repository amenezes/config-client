"""Core functions."""

from functools import wraps


def singleton(cls):
    """Ensure singleton instance."""
    instances = {}

    @wraps(cls)
    def instance():
        """Create class instance."""
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return instance
