"""Singleton metaclass implementation."""

from typing import Any


class SingletonMeta(type):
    """Metaclass for implementing singleton pattern.

    This metaclass ensures that only one instance of a class exists.
    """

    _instances: dict[type[Any], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create or return the singleton instance."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
