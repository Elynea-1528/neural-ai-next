"""Dependency injection konténer implementáció."""

import logging
import sys
import threading
import warnings
from collections.abc import Callable
from typing import TypeVar, cast

import structlog

from neural_ai.core.base.exceptions import ComponentNotFoundError, SingletonViolationError

T = TypeVar("T")
InterfaceT = TypeVar("InterfaceT")


class LazyComponent[T]:
    """Lusta betöltésű komponensek wrapper osztálya.

    Ez az osztály biztosítja a komponensek lusta (lazy) betöltését,
    ami azt jelenti, hogy a komponens csak akkor jön létre, amikor
    először használják.
    """

    def __init__(self, factory_func: Callable[[], T]) -> None:
        """Inicializálja a lusta komponenst.

        Args:
            factory_func: A komponens létrehozásához használt factory függvény
        """
        self._factory_func = factory_func
        self._instance: T | None = None
        self._loaded: bool = False
        self._lock = threading.RLock()

    def get(self) -> T:
        """Lekéri a komponens példányt (lusta betöltéssel).

        Returns:
            A komponens példánya
        """
        with self._lock:
            if not self._loaded:
                self._instance = self._factory_func()
                self._loaded = True
        return self._instance  # type: ignore[return-value]

    @property
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy a komponens betöltődött-e már.

        Returns:
            True, ha a komponens már betöltődött, egyébként False
        """
        return self._loaded


class DIContainer:
    """Egyszerű dependency injection konténer.

    A konténer kezeli a komponensek közötti függőségeket és biztosítja
    azok megfelelő inicializálását.
    """

    def __init__(self) -> None:
        """Konténer inicializálása."""
        self._instances: dict[object, object] = {}
        self._factories: dict[object, Callable[[], object]] = {}
        self._lazy_components: dict[str, LazyComponent[object]] = {}
        self._logger = logging.getLogger(__name__)

    def register_instance(self, interface: InterfaceT, instance: InterfaceT) -> None:
        """Példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            instance: Az interfészt megvalósító példány
        """
        interface_name = getattr(interface, '__name__', str(interface))
        instance_name = type(instance).__name__
        self._logger.debug(f"DI: Regisztrálva -> {interface_name} ({instance_name})")
        self._instances[interface] = instance

    def register_factory(self, interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None:
        """Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            factory: Az interfész implementációját létrehozó factory függvény
        """
        interface_name = getattr(interface, '__name__', str(interface))
        factory_name = getattr(factory, '__name__', 'anonymous')
        self._logger.debug(f"DI: Factory regisztrálva -> {interface_name} ({factory_name})")
        self._factories[interface] = factory

    def resolve(self, interface: InterfaceT) -> InterfaceT | None:
        """Függőség feloldása.

        Args:
            interface: Az interfész típusa

        Returns:
            Az interfészhez tartozó példány vagy None
        """
        if interface in self._instances:
            instance = self._instances[interface]
            # Verify singleton pattern
            self._verify_singleton(instance, str(interface))
            return instance  # type: ignore

        if interface in self._factories:
            factory = self._factories[interface]
            instance = factory()
            self._instances[interface] = instance
            # Verify singleton pattern
            self._verify_singleton(instance, str(interface))
            return instance  # type: ignore

        return None

    def register_lazy(self, component_name: str, factory_func: Callable[[], T]) -> None:
        """Lusta betöltésű komponens regisztrálása.

        Args:
            component_name: A komponens neve
            factory_func: A komponenst létrehozó függvény

        Raises:
            ValueError: Ha a komponens név érvénytelen vagy a factory
                függvény nem hívható
        """
        if not component_name:
            raise ValueError("Component name must be a non-empty string")

        if not callable(factory_func):
            raise ValueError("Factory function must be callable")

        lazy_component = LazyComponent[T](factory_func)
        self._lazy_components[component_name] = cast(LazyComponent[object], lazy_component)
        self._logger.info(f"Registered lazy component: {component_name}")

    def get(self, component_name: str) -> object:
        """Komponens példány lekérése (lusta betöltés támogatással).

        Args:
            component_name: A lekérendő komponens neve

        Returns:
            A komponens példánya

        Raises:
            ComponentNotFoundError: Ha a komponens nem található
        """
        # Check regular instances first
        if component_name in self._instances:
            instance = self._instances[component_name]
            # Verify singleton pattern
            self._verify_singleton(instance, component_name)
            return instance

        # Check lazy components
        if component_name in self._lazy_components:
            lazy_component = self._lazy_components[component_name]
            instance = lazy_component.get()

            # Verify singleton pattern
            self._verify_singleton(instance, component_name)

            # Move to regular instances for faster access
            self._instances[component_name] = instance
            del self._lazy_components[component_name]

            return instance

        raise ComponentNotFoundError(f"Component '{component_name}' not found")

    def get_lazy_components(self) -> dict[str, bool]:
        """Get status of all lazy components.

        Returns:
            A dictionary where keys are component names and values
            indicate whether the component has been loaded
        """
        return {name: component.is_loaded for name, component in self._lazy_components.items()}

    def preload_components(self, component_names: list[str]) -> None:
        """Preload specific components.

        Args:
            component_names: List of component names to preload
        """
        for name in component_names:
            if name in self._lazy_components:
                self._logger.info(f"Preloading component: {name}")
                self.get(name)

    def clear(self) -> None:
        """Clear the container."""
        self._instances.clear()
        self._factories.clear()
        self._lazy_components.clear()

    def _verify_singleton(self, instance: object, component_name: str) -> None:
        """Verify that the instance follows singleton pattern.

        Args:
            instance: The instance to verify
            component_name: The name of the component

        Raises:
            UserWarning: If singleton pattern is not properly implemented
        """
        # 1. Init ellenőrzés (Mindenkinek kötelező)
        if not getattr(instance, "_initialized", False):
            warnings.warn(
                f"Instance of {type(instance).__name__} ({component_name}) is missing '_initialized' flag.",
                UserWarning,
                stacklevel=2,
            )

        # 2. Singleton ellenőrzés (Csak ha SingletonMeta-t használ)
        # Ha az osztálynak van _instances attribútuma (a SingletonMeta jele)
        if hasattr(type(instance), "_instances"):
            if not hasattr(type(instance), "_instance"):
                warnings.warn(
                    f"Singleton class {type(instance).__name__} is missing '_instance'.",
                    UserWarning,
                    stacklevel=2,
                )

    def _enforce_singleton(self, component_name: str, instance: object) -> None:
        """Enforce singleton pattern by preventing duplicate registration.

        Args:
            component_name: The name of the component
            instance: The instance being registered

        Raises:
            SingletonViolationError: If singleton pattern is violated
        """
        if component_name in self._instances:
            existing_instance = self._instances[component_name]
            if existing_instance is not instance:
                raise SingletonViolationError(
                    f"Component '{component_name}' already registered with different instance. "
                    "Singleton pattern violated."
                )

    def register(self, component_name: str, instance: object) -> None:
        """Komponens példány regisztrálása.

        Args:
            component_name: A komponens neve
            instance: A regisztrálandó példány

        Raises:
            ValueError: Ha a component_name érvénytelen vagy az instance None
            SingletonViolationError: Ha a singleton minta megsértésre kerül
        """
        if not component_name:
            raise ValueError("Component name must be a non-empty string")

        if instance is None:
            raise ValueError("Instance cannot be None")

        # Enforce singleton pattern
        self._enforce_singleton(component_name, instance)

        self._instances[component_name] = instance
        # Note: In a real implementation, you would log this action
        # For example: self._logger.info(f"Registered component: {component_name}")

    def get_memory_usage(self) -> dict[str, int | dict[str, int]]:
        """Get memory usage statistics."""
        stats: dict[str, int | dict[str, int]] = {
            "total_instances": len(self._instances),
            "lazy_components": len(self._lazy_components),
            "loaded_lazy_components": sum(1 for c in self._lazy_components.values() if c.is_loaded),
            "instance_sizes": {},
        }

        # Calculate approximate sizes
        instance_sizes_dict = stats["instance_sizes"]
        assert isinstance(instance_sizes_dict, dict)
        for name, instance in self._instances.items():
            instance_sizes_dict[str(name)] = sys.getsizeof(instance)

        return stats
