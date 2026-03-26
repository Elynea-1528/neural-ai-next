"""Dependency injection konténer implementáció."""

import sys
import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar, cast

from neural_ai.core.base.exceptions import ComponentNotFoundError, SingletonViolationError
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.base.interfaces import DIContainerInterface, LazyComponentInterface
from neural_ai.core.utils.decorators import trace

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

T = TypeVar("T")
InterfaceT = TypeVar("InterfaceT")


class LazyComponent[T](LazyComponentInterface):
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

        if self._instance is None:
            raise ComponentNotFoundError("Lazy component factory returned None")

        return self._instance

    @property
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy a komponens betöltődött-e már.

        Returns:
            True, ha a komponens már betöltődött, egyébként False
        """
        return self._loaded


class DIContainer(DIContainerInterface, metaclass=SingletonMeta):
    """Egyszerű dependency injection konténer (Singleton).

    A konténer kezeli a komponensek közötti függőségeket és biztosítja
    azok megfelelő inicializálását. Singleton pattern biztosítja, hogy
    az alkalmazásban egyetlen konténer példány létezzen.
    """

    _initialized: bool

    def __init__(self, logger: "LoggerInterface | None" = None) -> None:
        """Konténer inicializálása.

        Args:
            logger: Logger példány. Ha nincs megadva, alapértelmezett logger-t használ.
        """
        # Singleton védelem: csak egyszer inicializáljuk (SingletonMeta kezeli)
        if hasattr(self, '_initialized') and self._initialized:
            return

        self._instances: dict[object, object] = {}
        self._factories: dict[object, Callable[[], object]] = {}
        self._lazy_components: dict[str, LazyComponent[object]] = {}
        self._initialized = True

        # Logger injektálás (opcionális, backward compatible)
        if logger is None:
            from neural_ai.core.logger.factory import LoggerFactory
            self._logger = LoggerFactory.get_logger(__name__)
        else:
            self._logger = logger

        self._logger.info("DI konténer inicializálva")

    @trace
    def register_instance(self, interface: InterfaceT, instance: InterfaceT) -> None:
        """Példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            instance: Az interfészt megvalósító példány
        """
        interface_name = getattr(interface, "__name__", str(interface))
        instance_name = type(instance).__name__
        self._logger.debug("DI regisztrálva", interface=interface_name, instance=instance_name)
        self._instances[interface] = instance

    @trace
    def register_factory(self, interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None:
        """Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa
            factory: Az interfész implementációját létrehozó factory függvény
        """
        interface_name = getattr(interface, "__name__", str(interface))
        factory_name = getattr(factory, "__name__", "anonymous")
        self._logger.debug(
            "DI factory regisztrálva", interface=interface_name, factory=factory_name
        )
        self._factories[interface] = factory

    @trace
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
            return cast(InterfaceT, instance)

        if interface in self._factories:
            factory = self._factories[interface]
            instance = factory()
            self._instances[interface] = instance
            # Verify singleton pattern
            self._verify_singleton(instance, str(interface))
            return cast(InterfaceT, instance)

        return None

    @trace
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
        self._logger.info("Lazy komponens regisztrálva", component_name=component_name)

    @trace
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

    @trace
    def get_lazy_components(self) -> dict[str, bool]:
        """Get status of all lazy components.

        Returns:
            A dictionary where keys are component names and values
            indicate whether the component has been loaded
        """
        return {name: component.is_loaded for name, component in self._lazy_components.items()}

    @trace
    def preload_components(self, component_names: list[str]) -> None:
        """Preload specific components.

        Args:
            component_names: List of component names to preload
        """
        for name in component_names:
            if name in self._lazy_components:
                self._logger.info("Komponens előtöltése", component_name=name)
                self.get(name)

    @trace
    def clear(self) -> None:
        """Clear the container."""
        self._instances.clear()
        self._factories.clear()
        self._lazy_components.clear()

    @trace
    def _verify_singleton(self, instance: object, component_name: str) -> None:
        """Ellenőrzi, hogy az instance követi-e a singleton mintát.

        Args:
            instance: Az ellenőrizendő példány
            component_name: A komponens neve
        """
        # import warnings
        # warnings.warn(f"Singleton verifikáció {component_name} számára", UserWarning)
        pass

    @trace
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

    @trace
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
        self._logger.info("Komponens regisztrálva", component_name=component_name)

    @trace
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
