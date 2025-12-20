"""Core komponensek gyűjtemény."""

import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, Generic, Optional, TypeVar, cast

from neural_ai.core.base.factory import CoreComponentFactory

# Runtime importok a resolve() metódushoz
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# Körkörös importok elkerüléséhez
if TYPE_CHECKING:
    from neural_ai.core.base.container import DIContainer

T = TypeVar("T")


class LazyLoader(Generic[T]):
    """Drága erőforrások lusta betöltője."""

    def __init__(self, loader_func: Callable[[], T]) -> None:
        """Lustabetöltő inicializálása.

        Args:
            loader_func: A függvény, amit az erőforrás betöltéséhez hívunk
        """
        self._loader_func = loader_func
        self._loaded: bool = False
        self._value: T | None = None
        self._lock = threading.RLock()

    def _load(self) -> T:
        """Betölti az erőforrást, ha még nincs betöltve."""
        with self._lock:
            if not self._loaded:
                self._value = self._loader_func()
                self._loaded = True
                assert self._value is not None, "Loader function returned None"
        return cast(T, self._value)

    def __call__(self) -> T:
        """Visszaadja a betöltött erőforrást."""
        return self._load()

    @property
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy az erőforrás betöltődött-e."""
        return self._loaded

    def reset(self) -> None:
        """Visszaállítja a betöltőt, hogy kirakja az erőforrást."""
        with self._lock:
            self._loaded = False
            self._value = None


class CoreComponents:
    """Alap komponensek lusta betöltéssel."""

    def __init__(self, container: Optional["DIContainer"] = None):
        """Alap komponensek inicializálása.

        Args:
            container: Egy függőséginjektáló konténer (opcionális)
        """
        # Körkörös import elkerüléséhez
        from neural_ai.core.base.container import DIContainer

        self._container = container or DIContainer()
        self._factory = CoreComponentFactory(self._container)

    @property
    def config(self) -> Optional["ConfigManagerInterface"]:
        """Config manager lekérése.

        Returns:
            ConfigManagerInterface vagy None, ha nincs regisztrálva
        """
        return self._container.resolve(ConfigManagerInterface)

    @property
    def logger(self) -> Optional["LoggerInterface"]:
        """Logger lekérése.

        Returns:
            LoggerInterface vagy None, ha nincs regisztrálva
        """
        return self._container.resolve(LoggerInterface)

    @property
    def storage(self) -> Optional["StorageInterface"]:
        """Storage lekérése.

        Returns:
            StorageInterface vagy None, ha nincs regisztrálva
        """
        return self._container.resolve(StorageInterface)

    def set_config(self, config: "ConfigManagerInterface") -> None:
        """Beállítja a config komponenst (csak teszteléshez).

        Args:
            config: A config manager implementáció
        """
        self._container.register_instance(ConfigManagerInterface, config)

    def set_logger(self, logger: "LoggerInterface") -> None:
        """Beállítja a logger komponenst (csak teszteléshez).

        Args:
            logger: A logger implementáció
        """
        self._container.register_instance(LoggerInterface, logger)

    def set_storage(self, storage: "StorageInterface") -> None:
        """Beállítja a storage komponenst (csak teszteléshez).

        Args:
            storage: A storage implementáció
        """
        self._container.register_instance(StorageInterface, storage)

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
