"""Dependency injection konténer implementáció."""

from typing import Any, Dict, Optional, TypeVar, cast

T = TypeVar("T")
InterfaceT = TypeVar("InterfaceT")


class DIContainer:
    """Egyszerű dependency injection konténer.

    A konténer kezeli a komponensek közötti függőségeket és biztosítja
    azok megfelelő inicializálását.
    """

    def __init__(self) -> None:
        """Konténer inicializálása."""
        self._instances: Dict[Any, Any] = {}
        self._factories: Dict[Any, Any] = {}

    def register_instance(self, interface: Any, instance: Any) -> None:
        """Példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            instance: A példány, ami implementálja az interfészt
        """
        self._instances[interface] = instance

    def register_factory(self, interface: Any, factory: Any) -> None:
        """Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            factory: A factory függvény az interfész implementáció létrehozásához
        """
        self._factories[interface] = factory

    def resolve(self, interface: Any) -> Optional[Any]:
        """Függőség feloldása.

        Args:
            interface: Az interfész típusa

        Returns:
            Az interfészhez tartozó példány vagy None
        """
        if interface in self._instances:
            return cast(Any, self._instances[interface])

        if interface in self._factories:
            instance = self._factories[interface]()
            self._instances[interface] = instance
            return cast(Any, instance)

        return None

    def clear(self) -> None:
        """Konténer ürítése."""
        self._instances.clear()
        self._factories.clear()
