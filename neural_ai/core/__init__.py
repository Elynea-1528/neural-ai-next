"""Neural-AI-Next core komponensek inicializációs modul.

Ez a modul a rendszer alapvető infrastrukturális komponenseit tartalmazza:
- Logger rendszer
- Konfiguráció kezelés
- Adattárolás
- Rendszer monitorozás

A modul biztosítja a core komponensek megfelelő inicializálását és
függőségi injektálását, elkerülve a körkörös függőségeket.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.config.interfaces.config_interface import (
        ConfigManagerInterface,  # noqa: F401
    )
    from neural_ai.core.db.implementations.sqlalchemy_session import DatabaseManager  # noqa: F401
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface  # noqa: F401
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface  # noqa: F401
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface  # noqa: F401
    from neural_ai.core.storage.services.market_data_persister import MarketDataPersister  # noqa: F401
    from neural_ai.core.system.interfaces.health_interface import (
        HealthMonitorInterface,  # noqa: F401
    )
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface  # noqa: F401


def get_version() -> str:
    """Dynamikusan betölti a csomag verzióját.

    Returns:
        A csomag verziója stringként. Ha a verzió nem érhető el,
        'unknown' értékkel tér vissza.
    """
    try:
        from importlib import metadata

        return metadata.version("neural-ai-next")
    except Exception:
        return "unknown"


def get_schema_version() -> str:
    """Visszaadja az aktuális séma verziót.

    Returns:
        Az aktuális séma verziója stringként.
    """
    return "1.0.0"


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
    from neural_ai.core.storage.factory import StorageFactory
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
    from neural_ai.core.storage.services.market_data_persister import MarketDataPersister
    from neural_ai.core.system.factory import SystemComponentFactory
    from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
    from neural_ai.core.utils.factory import HardwareFactory
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

    # DI container létrehozása
    container = DIContainer()
    
    # Ideiglenes logger a bootstrap folyamat elejéhez
    print("🚀 Neural AI Next - Rendszer indítása...")

    # 1. Konfiguráció létrehozása (először, hogy legyen konfig a loggernek)
    print("⏳ 1. Konfiguráció betöltése...")
    config = ConfigManagerFactory.create_manager("yaml")
    # Betöltjük a configs/ mappát
    config.load_directory("configs")
    container.register_instance(ConfigManagerInterface, config)
    print("   ✅ Config betöltve")

    # 2. Logger inicializálása a konfiggal
    print("⏳ 2. Logger konfigurálása...")
    logging_config = config.get_section("logging") or {}
    LoggerFactory.configure(logging_config)
    # Alap logger példány létrehozása
    logger = LoggerFactory.get_logger(name="NeuralAI.Bootstrap", logger_type="default")
    container.register_instance(LoggerInterface, logger)
    
    # Visszajelzés az előző lépésekről
    logger.info("🚀 Rendszer indítása...")
    logger.debug("✅ 1. Hardver: Detektálva")
    logger.debug("✅ 2. Config: Betöltve")
    logger.debug("✅ 3. Logger: Konfigurálva")

    # 3. Hardware inicializálása
    logger.info("⏳ 4. Hardver információ gyűjtése...")
    hardware = HardwareFactory.get_hardware_info()
    container.register_instance(HardwareInterface, hardware)
    logger.debug("-> Hardver manager regisztrálva")

    # 4. Adatbázis inicializálása (Config+Logger)
    logger.info("⏳ 5. Adatbázis indítása...")
    # Helyesen a DatabaseFactory-t használjuk, és átadjuk a már betöltött configot
    database = DatabaseFactory.create_manager(config_manager=config)
    container.register_instance(DatabaseManager, database)
    logger.debug("-> Adatbázis manager regisztrálva")

    # 5. EventBus inicializálása (Config+Logger)
    logger.info("⏳ 6. EventBus indítása...")
    event_bus = EventBusFactory.create_from_config(config)
    container.register_instance(EventBusInterface, event_bus)
    logger.debug("-> EventBus regisztrálva")

    # 6. Storage inicializálása (Config+Logger+HardwareInfo)
    logger.info("⏳ 7. Storage indítása...")
    storage_conf = config.get("storage") or {} # Szekció lekérése
    storage_type = storage_conf.get("type", "file") # Típus (file/parquet)

    storage = StorageFactory.get_storage(
        storage_type=storage_type,
        base_path=storage_conf.get("base_path"),
        logger=logger,
        hardware=hardware
    )
    container.register_instance(StorageInterface, storage)
    logger.debug(f"-> Storage engine: {storage_type}")

    # 7. Rendszer monitorozás inicializálása
    logger.info("⏳ 8. Rendszer monitorozás indítása...")
    health_monitor = SystemComponentFactory.create_health_monitor(
        name="core", logger=logger
    )
    container.register_instance(HealthMonitorInterface, health_monitor)
    logger.debug("-> Health monitor regisztrálva")
    
    # 8. MarketDataPersister inicializálása
    logger.info("⏳ 9. MarketDataPersister indítása...")
    market_data_persister = MarketDataPersister(
        event_bus=event_bus,
        storage=storage,
        logger=logger
    )
    container.register_instance(MarketDataPersister, market_data_persister)
    logger.debug("-> MarketDataPersister regisztrálva")
    
    # 9. JForex Live Feed inicializálása (ha engedélyezve van)
    logger.info("⏳ 10. JForex Live Feed ellenőrzése...")
    live_conf = config.get("jforex_live") or {}
    if live_conf.get("enabled", False):
        from neural_ai.collectors.jforex.factory import JForexFactory
        from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
        
        live_feed = JForexFactory.create_live_feed(config, logger, event_bus)
        container.register_instance(ILiveFeed, live_feed)
        logger.info("✅ JForex Live Feed inicializálva")
    else:
        logger.debug("-> JForex Live Feed nincs engedélyezve")
    
    logger.info("✅ RENDSZER ÜZEMKÉSZ")
    
    return CoreComponents(container=container)


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
    if not hasattr(get_core_components, "_instance"):
        get_core_components._instance = bootstrap_core()  # type: ignore

    return get_core_components._instance  # type: ignore


# Publikus interfészek exportálása a könnyű hozzáférés érdekében
__all__ = [
    "bootstrap_core",
    "get_core_components",
    "get_version",
    "get_schema_version",
]
