"""Core komponensek gyűjtemény."""

import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, Optional, TypeVar, cast

from neural_ai.core.base.factory import CoreComponentFactory

# Körkörös importok elkerüléséhez
if TYPE_CHECKING:
    from neural_ai.core.base.implementations.di_container import DIContainer
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.implementations.zeromq_bus import EventBus
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
    from neural_ai.core.utils.implementations.hardware_info import HardwareInfo

T = TypeVar("T")


class LazyLoader[T]:
    """Drága erőforrások lusta betöltője."""

    def __init__(self, loader_func: Callable[[], T]) -> None:
        """Lustabetöltő inicializálása.

        Args:
            loader_func: A függvény, amely az erőforrás betöltését végzi.
        """
        self._loader_func = loader_func
        self._loaded: bool = False
        self._value: T | None = None
        self._lock = threading.RLock()

    def _load(self) -> T:
        """Betölti az erőforrást, ha még nincs betöltve.

        Returns:
            A betöltött erőforrás.
        """
        with self._lock:
            if not self._loaded:
                self._value = self._loader_func()
                self._loaded = True
                assert self._value is not None, "Loader function returned None"
        return cast(T, self._value)

    def __call__(self) -> T:
        """Visszaadja a betöltött erőforrást.

        Returns:
            A betöltött erőforrás.
        """
        return self._load()

    @property
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy az erőforrás betöltődött-e.

        Returns:
            True, ha az erőforrás betöltve van, különben False.
        """
        return self._loaded

    def reset(self) -> None:
        """Visszaállítja a betöltőt, hogy kirakja az erőforrást.

        Ez a metódus visszaállítja a betöltő állapotát, lehetővé téve
        az erőforrás újbóli betöltését.
        """
        with self._lock:
            self._loaded = False
            self._value = None


class CoreComponents:
    """Alap komponensek lusta betöltéssel."""

    def __init__(self, container: Optional["DIContainer"] = None):
        """Alap komponensek inicializálása.

        Args:
            container: Egy függőséginjektáló konténer példány.
                       Ha nincs megadva, új konténert hoz létre.
        """
        # Körkörös import elkerüléséhez
        from neural_ai.core.base.implementations.di_container import DIContainer

        self._container = container or DIContainer()
        self._factory = CoreComponentFactory(self._container)

    @property
    def config(self) -> Optional["ConfigManagerInterface"]:
        """Konfiguráció kezelő komponens lekérése.

        Returns:
            A konfiguráció kezelő példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        result = self._container.resolve(ConfigManagerInterface)
        return cast(Optional["ConfigManagerInterface"], result)

    @property
    def logger(self) -> Optional["LoggerInterface"]:
        """Naplózó komponens lekérése.

        Returns:
            A naplózó példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        result = self._container.resolve(LoggerInterface)
        return cast(Optional["LoggerInterface"], result)

    @property
    def storage(self) -> Optional["StorageInterface"]:
        """Tároló komponens lekérése.

        Returns:
            A tároló példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        result = self._container.resolve(StorageInterface)
        return cast(Optional["StorageInterface"], result)

    @property
    def database(self) -> Optional["DatabaseManager"]:
        """Adatbázis komponens lekérése.

        Returns:
            Az adatbázis példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
        result = self._container.resolve(DatabaseManager)
        return cast(Optional["DatabaseManager"], result)

    @property
    def event_bus(self) -> Optional["EventBus"]:
        """Esemény busz komponens lekérése.

        Returns:
            Az esemény busz példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.events.implementations.zeromq_bus import EventBus
        result = self._container.resolve(EventBus)
        return cast(Optional["EventBus"], result)

    @property
    def hardware(self) -> Optional["HardwareInfo"]:
        """Hardver információ komponens lekérése.

        Returns:
            A hardver információ példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
        result = self._container.resolve(HardwareInfo)
        return cast(Optional["HardwareInfo"], result)

    def set_config(self, config: "ConfigManagerInterface") -> None:
        """Beállítja a konfiguráció komponenst (csak teszteléshez).

        Args:
            config: A konfiguráció kezelő implementáció példánya.
        """
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        self._container.register_instance(ConfigManagerInterface, config)

    def set_logger(self, logger: "LoggerInterface") -> None:
        """Beállítja a naplózó komponenst (csak teszteléshez).

        Args:
            logger: A naplózó implementáció példánya.
        """
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        self._container.register_instance(LoggerInterface, logger)

    def set_storage(self, storage: "StorageInterface") -> None:
        """Beállítja a tároló komponenst (csak teszteléshez).

        Args:
            storage: A tároló implementáció példánya.
        """
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        self._container.register_instance(StorageInterface, storage)

    def set_database(self, database: "DatabaseManager") -> None:
        """Beállítja az adatbázis komponenst (csak teszteléshez).

        Args:
            database: Az adatbázis implementáció példánya.
        """
        from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
        self._container.register_instance(DatabaseManager, database)

    def set_event_bus(self, event_bus: "EventBus") -> None:
        """Beállítja az esemény busz komponenst (csak teszteléshez).

        Args:
            event_bus: Az esemény busz implementáció példánya.
        """
        from neural_ai.core.events.implementations.zeromq_bus import EventBus
        self._container.register_instance(EventBus, event_bus)

    def set_hardware(self, hardware: "HardwareInfo") -> None:
        """Beállítja a hardver információ komponenst (csak teszteléshez).

        Args:
            hardware: A hardver információ implementáció példánya.
        """
        from neural_ai.core.utils.implementations.hardware_info import HardwareInfo
        self._container.register_instance(HardwareInfo, hardware)

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

    def has_database(self) -> bool:
        """Ellenőrzi, hogy van-e database komponens.

        Returns:
            bool: True ha van database komponens, False ha nincs
        """
        return self.database is not None

    def has_event_bus(self) -> bool:
        """Ellenőrzi, hogy van-e event_bus komponens.

        Returns:
            bool: True ha van event_bus komponens, False ha nincs
        """
        return self.event_bus is not None

    def has_hardware(self) -> bool:
        """Ellenőrzi, hogy van-e hardware komponens.

        Returns:
            bool: True ha van hardware komponens, False ha nincs
        """
        return self.hardware is not None

    def validate(self) -> bool:
        """Ellenőrzi, hogy minden szükséges komponens megvan-e.

        Returns:
            bool: True ha minden komponens megvan, False ha valamelyik hiányzik
        """
        return all([
            self.has_config(),
            self.has_logger(),
            self.has_storage(),
            self.has_database(),
            self.has_event_bus(),
            self.has_hardware()
        ])
