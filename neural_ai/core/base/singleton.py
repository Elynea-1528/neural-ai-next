"""Singleton metaclass megvalósítása."""

from typing import Any


class SingletonMeta(type):
    """Singleton minta megvalósítására szolgáló metaclass.

    Ez a metaclass biztosítja, hogy egy osztályból csak egy példány létezzen.
    """

    _instances: dict[type[Any], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Singleton példány létrehozása vagy visszaadása."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
