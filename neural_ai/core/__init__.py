"""Neural-AI-Next core komponensek inicializációs modul.

Ez a modul a rendszer alapvető infrastrukturális komponenseit tartalmazza:
- Logger rendszer
- Konfiguráció kezelés
- Adattárolás
- Rendszer monitorozás

A modul biztosítja a core komponensek megfelelő inicializálását és
függőségi injektálását, elkerülve a körkörös függőségeket.
"""

from typing import TYPE_CHECKING, Any, cast

from neural_ai.core.config.interfaces.types import (
    IngestionConfig,
    JForexLiveConfig,
    LoggingConfig,
    StorageConfig,
)
from neural_ai.core.utils.decorators import trace

if TYPE_CHECKING:
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.config.interfaces.config_interface import (
        ConfigManagerInterface,
    )
    from neural_ai.core.db.implementations.sqlalchemy_session import (
        DatabaseManager,
    )
    from neural_ai.core.events.interfaces.event_bus_interface import (
        EventBusInterface,
    )
    from neural_ai.core.logger.interfaces.logger_interface import (
        LoggerInterface,
    )
    from neural_ai.core.system.interfaces.health_interface import (
        HealthMonitorInterface,
    )
    from neural_ai.core.utils.interfaces.hardware_interface import (
        HardwareInterface,
    )
    from neural_ai.data.ingestion.market_data_persister import (
        MarketDataPersister,
    )
    from neural_ai.data.storage.interfaces.storage_interface import (
        StorageInterface,
    )


@trace
def get_version() -> str:
    """Dynamikusan betölti a csomag verzióját.

    Returns:
        A csomag verziója stringként. Ha a verzió nem érhető el,
        'unknown' értékkel tér vissza.
    """
    try:
        from importlib import metadata

        return metadata.version("neural-ai-next")
    except Exception:  # PackageNotFoundError vagy ImportError
        return "unknown"


@trace
def get_schema_version() -> str:
    """Visszaadja az aktuális séma verziót.

    Returns:
        Az aktuális séma verziója stringként.
    """
    return "1.0.0"


@trace
def bootstrap_core(
    config_path: str | None = None, log_level: str | None = None
) -> "CoreComponents":
    """Bootstrap funkció a core komponensek inicializálásához.

    Ez a függvény biztosítja a core komponensek megfelelő sorrendű
    inicializálását, elkerülve a körkörös függőségeket.

    A bootstrap folyamat:
    1. HardwareFactory - Hardver információk lekérdezése
    2. ConfigFactory - Konfiguráció betöltése
    3. LoggerFactory - Logger inicializálása a konfiguráció alapján
    4. DatabaseFactory - Adatbázis kapcsolat létrehozása (Config+Logger)
    5. EventBusFactory - Esemény busz inicializálása (Config+Logger)
    6. StorageFactory - Tárhely inicializálása (Config+Logger+HardwareInfo)
    7. SystemFactory - Rendszer monitorozás (Config+Logger)

    Args:
        config_path: Opcionális konfigurációs fájl útvonala. Ha None, akkor
            a 'configs' könyvtárat tölti be.
        log_level: Opcionális log szint beállítás. Ha None, akkor a konfigurációból
            olvassa ki.

    Returns:
        A teljesen inicializált CoreComponents példány

    Raises:
        ConfigError: Ha a konfiguráció betöltése sikertelen
        LoggerError: Ha a logger inicializálása sikertelen
        DatabaseError: Ha az adatbázis kapcsolat létrehozása sikertelen

    Example:
        >>> core = bootstrap_core()
        >>> core.logger.info("Alkalmazás elindult")
        >>> await core.database.initialize()
        >>> await core.event_bus.start()
    """
    # Importok a függőségi körkörök elkerüléséhez
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.base.implementations.di_container import DIContainer
    from neural_ai.core.config.factory import ConfigManagerFactory
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.db.factory import DatabaseFactory
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager
    from neural_ai.core.events.factory import EventBusFactory
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.factory import LoggerFactory
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.system.factory import SystemComponentFactory
    from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
    from neural_ai.core.utils.factory import HardwareFactory
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
    from neural_ai.data.ingestion.market_data_persister import MarketDataPersister
    from neural_ai.data.storage.factory import StorageFactory
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

    # DI container létrehozása
    container = DIContainer()

    # 1. Konfiguráció létrehozása (először, hogy legyen konfig a loggernek)
    # Betöltjük a configs/ mappát vagy a megadott útvonalat
    path_to_load = config_path if config_path else "configs"
    try:
        config = ConfigManagerFactory.create_manager("yaml")
        config.load_directory(path_to_load)
        container.register_instance(ConfigManagerInterface, config)
    except Exception as e:
        from neural_ai.core.config.exceptions.config_error import ConfigLoadError

        raise ConfigLoadError(f"Failed to load configuration from {path_to_load}: {e}") from e

    # 2. Logger inicializálása a konfiggal
    logging_config_dict = config.get_section("logging") or {}
    logging_config = LoggingConfig(**logging_config_dict)
    LoggerFactory.configure(logging_config.model_dump(exclude_none=True))
    # Alap logger példány létrehozása
    logger = LoggerFactory.get_logger(__name__, logger_type="default")
    container.register_instance(LoggerInterface, logger)

    # Visszajelzés az előző lépésekről
    logger.info("🚀 Neural AI Next - Rendszer indítása...")
    logger.info("⏳ 1. Konfiguráció betöltése...")
    logger.debug("✅ 1. Config: Betöltve")
    logger.debug("✅ 2. Logger: Konfigurálva")

    # 3. Hardware inicializálása
    logger.info("⏳ 4. Hardver információ gyűjtése...")
    hardware = HardwareFactory.get_hardware_info()
    container.register_instance(HardwareInterface, hardware)
    logger.debug("-> Hardver manager regisztrálva")

    # 4. Adatbázis inicializálása (Config+Logger)
    logger.info("⏳ 5. Adatbázis indítása...")
    # DatabaseFactory példányosítása DI-val
    db_factory = DatabaseFactory(logger=logger, config_manager=config)
    database = db_factory.create_manager()
    container.register_instance(DatabaseManager, database)
    logger.debug("-> Adatbázis manager regisztrálva")

    # 5. EventBus inicializálása (Config+Logger)
    logger.info("⏳ 6. EventBus indítása...")
    event_bus_factory = EventBusFactory(logger, config)
    event_bus = event_bus_factory.create_from_config()
    container.register_instance(EventBusInterface, event_bus)
    logger.debug("-> EventBus regisztrálva")

    # 6. Storage inicializálása (Config+Logger+HardwareInfo)
    logger.info("⏳ 7. Storage indítása...")
    storage_conf_dict = cast(dict[str, Any], config.get("storage") or {})
    storage_conf = StorageConfig(**storage_conf_dict)  # Validáció Pydantic modellel
    storage_type = storage_conf.type or "parquet"  # Default a modellben

    try:
        storage = StorageFactory.get_storage(
            storage_type=storage_type,
            base_path=storage_conf.base_path,
            logger=logger,
            config=config,
            hardware=hardware,
        )
        container.register_instance(StorageInterface, storage)
        logger.debug(f"-> Storage engine: {storage_type}")
    except Exception:
        logger.critical("Storage init failed", exc_info=True)
        raise

    # 7. Rendszer monitorozás inicializálása
    logger.info("⏳ 8. Rendszer monitorozás indítása...")
    health_monitor = SystemComponentFactory.create_health_monitor(name="core", logger=logger)

    # Komponensek regisztrálása a health monitor-ba
    SystemComponentFactory.register_component(
        monitor_name="core", component_name="core", health_check=None
    )
    SystemComponentFactory.register_component(
        monitor_name="core", component_name="database", health_check=None
    )
    SystemComponentFactory.register_component(
        monitor_name="core", component_name="event_bus", health_check=None
    )
    SystemComponentFactory.register_component(
        monitor_name="core", component_name="collectors", health_check=None
    )
    SystemComponentFactory.register_component(
        monitor_name="core", component_name="storage", health_check=None
    )

    container.register_instance(HealthMonitorInterface, health_monitor)
    logger.debug("-> Health monitor regisztrálva")

    # 8. MarketDataPersister inicializálása
    logger.info("⏳ 9. MarketDataPersister indítása...")
    ingestion_config = cast(IngestionConfig, config.get_section("ingestion") or {})
    market_data_persister = MarketDataPersister(
        event_bus=event_bus,
        storage=storage,
        logger=logger,
        config=ingestion_config,
    )
    container.register_instance(MarketDataPersister, market_data_persister)
    logger.debug("-> MarketDataPersister regisztrálva")

    # 9. JForex Live Feed inicializálása (ha engedélyezve van)
    logger.info("⏳ 10. JForex Live Feed ellenőrzése...")
    # Figyelem: A collectors.yaml tartalma a 'collectors' kulcs alatt van!
    live_conf_dict = cast(dict[str, Any], config.get("collectors", "jforex_live") or {})
    live_conf = JForexLiveConfig(**live_conf_dict)

    if live_conf.enabled:
        from neural_ai.collectors.jforex.factory import JForexFactory
        from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed

        live_feed = JForexFactory.create_live_feed(config, logger, event_bus)
        container.register_instance(ILiveFeed, live_feed)
        logger.info("✅ JForex Live Feed inicializálva")
    else:
        logger.debug("-> JForex Live Feed nincs engedélyezve")

    logger.info("✅ RENDSZER ÜZEMKÉSZ")

    return CoreComponents(container=container)


# Globális változó a singleton példány tárolására
_core_components_instance: "CoreComponents | None" = None


@trace
def get_core_components() -> "CoreComponents":
    """Globális core komponensek lekérdezése.

    Ez a függvény egy szingleton példányt ad vissza a core komponensekből,
    biztosítva, hogy az alkalmazás egészében ugyanazok a komponensek
    legyenek elérhetőek.

    Returns:
        A globális CoreComponents példány

    Example:
        >>> core = get_core_components()
        >>> core.logger.info("Komponens használatban")
    """
    global _core_components_instance
    if _core_components_instance is None:
        _core_components_instance = bootstrap_core()

    return _core_components_instance


# Publikus interfészek exportálása a könnyű hozzáférés érdekében
__all__ = [
    "bootstrap_core",
    "get_core_components",
    "get_version",
    "get_schema_version",
    "ConfigManagerInterface",
    "DatabaseManager",
    "EventBusInterface",
    "LoggerInterface",
    "HealthMonitorInterface",
    "HardwareInterface",
    "MarketDataPersister",
    "StorageInterface",
]
