"""Core komponensek gyűjtemény."""

import threading
from functools import wraps
from typing import Callable, Generic, Optional, TypeVar, cast

from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

T = TypeVar("T")


class LazyLoader(Generic[T]):
    """Lazy loader for expensive resources."""

    def __init__(self, loader_func: Callable[[], T]) -> None:
        """
        Initialize lazy loader.

        Args:
            loader_func: Function to call when loading the resource
        """
        self._loader_func = loader_func
        self._loaded: bool = False
        self._value: Optional[T] = None
        self._lock = threading.RLock()

    def _load(self) -> T:
        """Load the resource if not already loaded."""
        with self._lock:
            if not self._loaded:
                self._value = self._loader_func()
                self._loaded = True
                assert self._value is not None, "Loader function returned None"
        return cast(T, self._value)

    def __call__(self) -> T:
        """Get the loaded resource."""
        return self._load()

    @property
    def is_loaded(self) -> bool:
        """Check if the resource is loaded."""
        return self._loaded

    def reset(self) -> None:
        """Reset the loader to unload the resource."""
        with self._lock:
            self._loaded = False
            self._value = None


def lazy_property(func: Callable[..., T]) -> property:
    """Create lazy-loaded property decorator."""
    attr_name = f"_lazy_{func.__name__}"

    @property
    @wraps(func)
    def wrapper(instance: object) -> T:
        if not hasattr(instance, attr_name):
            value = func(instance)
            setattr(instance, attr_name, value)
        return getattr(instance, attr_name)

    return wrapper


class CoreComponents:
    """Core components with lazy loading support."""

    def __init__(self, container: Optional[DIContainer] = None):
        """Initialize core components."""
        from neural_ai.core.base.container import DIContainer

        self._container = container or DIContainer()
        self._factory = CoreComponentFactory(self._container)


    @property
    def config(self) -> Optional[ConfigManagerInterface]:
        """Get config manager."""
        return self._container.resolve(ConfigManagerInterface)

    @property
    def logger(self) -> Optional[LoggerInterface]:
        """Get logger."""
        return self._container.resolve(LoggerInterface)

    @property
    def storage(self) -> Optional[StorageInterface]:
        """Get storage."""
        return self._container.resolve(StorageInterface)


    def has_config(self) -> bool:
        """Ellenőrzi, hogy van-e config komponens.

        Returns:
            bool: True ha van config komponens, False ha nincs
        """
        return self.config is not None

    def has_logger(self) -> bool:
        """Ellenőrzi, hogy van-e logger komponens.

        Returns:
            bool: True ha van logger komponens, False ha nincs
        """
        return self.logger is not None

    def has_storage(self) -> bool:
        """Ellenőrzi, hogy van-e storage komponens.

        Returns:
            bool: True ha van storage komponens, False ha nincs
        """
        return self.storage is not None

    def validate(self) -> bool:
        """Ellenőrzi, hogy minden szükséges komponens megvan-e.

        Returns:
            bool: True ha minden komponens megvan, False ha valamelyik hiányzik
        """
        return all([self.has_config(), self.has_logger(), self.has_storage()])
