"""Core functions."""


def singleton(cls):
    """Ensure singleton instance."""
    instances = {}

    def instance():
        """Create class instance."""
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return instance
