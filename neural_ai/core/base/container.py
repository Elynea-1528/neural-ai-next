"""Dependency injection konténer implementáció."""

import logging
import sys
import threading
import warnings
from typing import Any, Callable, Dict, List, Optional, TypeVar

from neural_ai.core.base.exceptions import (
    ComponentNotFoundError,
    SingletonViolationError,
)

T = TypeVar("T")
InterfaceT = TypeVar("InterfaceT")


class LazyComponent:
    """Lusta betöltésű komponensek wrapper osztálya.

    Ez az osztály biztosítja a komponensek lusta (lazy) betöltését,
    ami azt jelenti, hogy a komponens csak akkor jön létre, amikor
    először használják.
    """

    def __init__(self, factory_func: Callable[[], Any]) -> None:
        """Inicializálja a lusta komponenst.

        Args:
            factory_func: A komponens létrehozásához használt factory függvény
        """
        self._factory_func = factory_func
        self._instance: Optional[Any] = None
        self._loaded: bool = False
        self._lock = threading.RLock()

    def get(self) -> Any:
        """Lekéri a komponens példányt (lusta betöltéssel).

        Returns:
            A komponens példánya
        """
        with self._lock:
            if not self._loaded:
                self._instance = self._factory_func()
                self._loaded = True
        return self._instance

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
        self._instances: Dict[Any, Any] = {}
        self._factories: Dict[Any, Any] = {}
        self._lazy_components: Dict[str, LazyComponent] = {}
        self._logger = logging.getLogger(__name__)

    def register_instance(self, interface: Any, instance: Any) -> None:
        """Register an instance in the container.

        Args:
            interface: The interface type
            instance: The instance implementing the interface
        """
        self._instances[interface] = instance

    def register_factory(self, interface: Any, factory: Any) -> None:
        """Register a factory function in the container.

        Args:
            interface: The interface type
            factory: Factory function to create interface implementation
        """
        self._factories[interface] = factory

    def resolve(self, interface: Any) -> Optional[Any]:
        """Resolve a dependency.

        Args:
            interface: The interface type

        Returns:
            The instance for the interface or None
        """
        if interface in self._instances:
            instance = self._instances[interface]
            # Verify singleton pattern
            self._verify_singleton(instance, str(interface))
            return instance

        if interface in self._factories:
            instance = self._factories[interface]()
            self._instances[interface] = instance
            # Verify singleton pattern
            self._verify_singleton(instance, str(interface))
            return instance

        return None

    def register_lazy(
        self, component_name: str, factory_func: Callable[[], Any]
    ) -> None:
        """Register a lazy-loaded component.

        Args:
            component_name: The component name
            factory_func: Function to create the component

        Raises:
            ValueError: If component name is invalid or factory
                function is not callable
        """
        if not component_name:
            raise ValueError("Component name must be a non-empty string")

        if not callable(factory_func):
            raise ValueError("Factory function must be callable")

        lazy_component = LazyComponent(factory_func)
        self._lazy_components[component_name] = lazy_component
        self._logger.info(f"Registered lazy component: {component_name}")

    def get(self, component_name: str) -> Any:
        """Get a component instance (with lazy loading support).

        Args:
            component_name: The name of the component to retrieve

        Returns:
            The component instance

        Raises:
            ComponentNotFoundError: If the component is not found
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

    def get_lazy_components(self) -> Dict[str, bool]:
        """Get status of all lazy components.

        Returns:
            A dictionary where keys are component names and values
            indicate whether the component has been loaded
        """
        return {
            name: component.is_loaded
            for name, component in self._lazy_components.items()
        }

    def preload_components(self, component_names: List[str]) -> None:
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

    def _verify_singleton(self, instance: Any, component_name: str) -> None:
        """Verify that the instance follows singleton pattern.

        Args:
            instance: The instance to verify
            component_name: The name of the component

        Raises:
            UserWarning: If singleton pattern is not properly implemented
        """
        # Check if instance has _initialized flag
        if not hasattr(instance, "_initialized"):
            warnings.warn(
                f"Instance of {type(instance).__name__} (component: {component_name}) "
                "does not have _initialized flag. Singleton pattern may not be "
                "properly implemented.",
                UserWarning,
                stacklevel=2,
            )

        # Check if instance has _instance class variable (class-level singleton)
        instance_type: type = type(instance)
        if not hasattr(instance_type, "_instance"):
            warnings.warn(
                f"Instance of {type(instance).__name__} (component: {component_name}) "
                "does not have _instance class variable. Consider implementing "
                "proper singleton pattern.",
                UserWarning,
                stacklevel=2,
            )

        # Check if instance is properly registered
        if component_name not in self._instances:
            warnings.warn(
                f"Component {component_name} not properly registered in container. "
                "Singleton pattern may be compromised.",
                UserWarning,
                stacklevel=2,
            )

    def _enforce_singleton(self, component_name: str, instance: Any) -> None:
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

    def register(self, component_name: str, instance: Any) -> None:
        """Register a component instance.

        Args:
            component_name: The name of the component
            instance: The instance to register

        Raises:
            ValueError: If component_name is invalid or instance is None
            SingletonViolationError: If singleton pattern is violated
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

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        stats: Dict[str, Any] = {
            "total_instances": len(self._instances),
            "lazy_components": len(self._lazy_components),
            "loaded_lazy_components": sum(1 for c in self._lazy_components.values() if c.is_loaded),
            "instance_sizes": {},
        }

        # Calculate approximate sizes
        for name, instance in self._instances.items():
            stats["instance_sizes"][str(name)] = sys.getsizeof(instance)

        return stats
