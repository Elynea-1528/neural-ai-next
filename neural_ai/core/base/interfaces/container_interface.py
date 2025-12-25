"""Dependency injection konténer interfészek.

Ez a modul tartalmazza a DI konténerhez és lusta betöltéshez kapcsolódó interfészeket.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")
InterfaceT = TypeVar("InterfaceT")


class DIContainerInterface(ABC):
    """Dependency injection konténer interfész.

    Ez az interfész definiálja a dependency injection konténer alapvető
    funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.
    """

    @abstractmethod
    def register_instance(self, interface: InterfaceT, instance: InterfaceT) -> None:
        """Komponens példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa, amihez a példányt regisztráljuk
            instance: A regisztrálandó példány
        """
        pass

    @abstractmethod
    def register_factory(self, interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None:
        """Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa, amihez a factory-t regisztráljuk
            factory: A factory függvény, ami létrehozza az implementációt
        """
        pass

    @abstractmethod
    def resolve(self, interface: InterfaceT) -> InterfaceT | None:
        """Függőség feloldása a konténerből.

        Args:
            interface: Az interfész típusa, amit fel szeretnénk oldani

        Returns:
            A regisztrált példány vagy None ha nem található
        """
        pass

    @abstractmethod
    def register_lazy(self, component_name: str, factory_func: Callable[[], T]) -> None:
        """Lusta betöltésű komponens regisztrálása.

        Args:
            component_name: A komponens neve
            factory_func: A komponens létrehozásához használt factory függvény

        Raises:
            ValueError: Ha a komponens név érvénytelen vagy a factory függvény nem hívható
        """
        pass

    @abstractmethod
    def get(self, component_name: str) -> object:
        """Komponens példány lekérése (lusta betöltéssel).

        Args:
            component_name: A lekérendő komponens neve

        Returns:
            A komponens példánya

        Raises:
            ComponentNotFoundError: Ha a komponens nem található
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Konténer ürítése."""
        pass


class LazyComponentInterface(ABC):
    """Lusta betöltésű komponens interfész.

    Ez az interfész definiálja a lusta (lazy) betöltésű komponensek
    alapvető funkcionalitását.
    """

    @abstractmethod
    def get(self) -> object:
        """Komponens példány lekérése (lusta betöltéssel).

        Returns:
            A komponens példánya
        """
        pass

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy a komponens betöltődött-e már.

        Returns:
            True, ha a komponens már betöltődött, egyébként False
        """
        pass
