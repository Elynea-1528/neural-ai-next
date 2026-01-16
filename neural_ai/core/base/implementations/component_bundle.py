"""Core komponensek gyűjtemény."""

from typing import TYPE_CHECKING, Optional, TypeVar

import structlog

from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.utils.decorators import trace

# Körkörös importok elkerüléséhez
if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
    from neural_ai.core.base.implementations.di_container import DIContainer
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.data.ingestion.market_data_persister import MarketDataPersister
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

T = TypeVar("T")


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
        self._logger = structlog.get_logger(__name__)

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

        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

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
    def event_bus(self) -> Optional["EventBusInterface"]:
        """Esemény busz komponens lekérése.

        Returns:
            Az esemény busz példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface

        result = self._container.resolve(EventBusInterface)
        return cast(Optional["EventBusInterface"], result)

    @property
    def hardware(self) -> Optional["HardwareInterface"]:
        """Hardver információ komponens lekérése.

        Returns:
            A hardver információ példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

        result = self._container.resolve(HardwareInterface)
        return cast(Optional["HardwareInterface"], result)

    @property
    def persister(self) -> Optional["MarketDataPersister"]:
        """Market data persister komponens lekérése.

        Returns:
            A market data persister példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.data.ingestion.market_data_persister import MarketDataPersister

        result = self._container.resolve(MarketDataPersister)
        return cast(Optional["MarketDataPersister"], result)

    @property
    def live_feed(self) -> Optional["ILiveFeed"]:
        """Live feed komponens lekérése.

        Returns:
            A live feed példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed

        result = self._container.resolve(ILiveFeed)
        return cast(Optional["ILiveFeed"], result)

    @property
    def health_monitor(self) -> Optional["HealthMonitorInterface"]:
        """Health monitor komponens lekérése.

        Returns:
            A health monitor példánya, vagy None ha nincs regisztrálva.
        """
        from typing import cast

        from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface

        result = self._container.resolve(HealthMonitorInterface)
        return cast(Optional["HealthMonitorInterface"], result)

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
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        self._container.register_instance(StorageInterface, storage)

    def set_database(self, database: "DatabaseManager") -> None:
        """Beállítja az adatbázis komponenst (csak teszteléshez).

        Args:
            database: Az adatbázis implementáció példánya.
        """
        from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager

        self._container.register_instance(DatabaseManager, database)

    def set_event_bus(self, event_bus: "EventBusInterface") -> None:
        """Beállítja az esemény busz komponenst (csak teszteléshez).

        Args:
            event_bus: Az esemény busz implementáció példánya.
        """
        from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface

        self._container.register_instance(EventBusInterface, event_bus)

    def set_hardware(self, hardware: "HardwareInterface") -> None:
        """Beállítja a hardver információ komponenst (csak teszteléshez).

        Args:
            hardware: A hardver információ implementáció példánya.
        """
        from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

        self._container.register_instance(HardwareInterface, hardware)

    def set_persister(self, persister: "MarketDataPersister") -> None:
        """Beállítja a market data persister komponenst (csak teszteléshez).

        Args:
            persister: A market data persister implementáció példánya.
        """
        from neural_ai.data.ingestion.market_data_persister import MarketDataPersister

        self._container.register_instance(MarketDataPersister, persister)

    def set_live_feed(self, live_feed: "ILiveFeed") -> None:
        """Beállítja a live feed komponenst (csak teszteléshez).

        Args:
            live_feed: A live feed implementáció példánya.
        """
        from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed

        self._container.register_instance(ILiveFeed, live_feed)

    def set_health_monitor(self, health_monitor: "HealthMonitorInterface") -> None:
        """Beállítja a health monitor komponenst (csak teszteléshez).

        Args:
            health_monitor: A health monitor implementáció példánya.
        """
        from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface

        self._container.register_instance(HealthMonitorInterface, health_monitor)

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

    def has_persister(self) -> bool:
        """Ellenőrzi, hogy van-e persister komponens.

        Returns:
            bool: True ha van persister komponens, False ha nincs
        """
        return self.persister is not None

    def has_live_feed(self) -> bool:
        """Ellenőrzi, hogy van-e live feed komponens.

        Returns:
            bool: True ha van live feed komponens, False ha nincs
        """
        return self.live_feed is not None

    def has_health_monitor(self) -> bool:
        """Ellenőrzi, hogy van-e health monitor komponens.

        Returns:
            bool: True ha van health monitor komponens, False ha nincs
        """
        return self.health_monitor is not None

    @trace
    def validate(self) -> bool:
        """Ellenőrzi, hogy minden szükséges komponens megvan-e.

        Returns:
            bool: True ha minden komponens megvan, False ha valamelyik hiányzik
        """
        return all(
            [
                self.has_config(),
                self.has_logger(),
                self.has_storage(),
                self.has_database(),
                self.has_event_bus(),
                self.has_hardware(),
                self.has_health_monitor(),
            ]
        )
