"""Core functions."""


def singleton(cls):
    """Ensure singleton instance."""
    instances = {}

    def instance(*args, **kwargs):
        """Create class instance."""
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return instance
