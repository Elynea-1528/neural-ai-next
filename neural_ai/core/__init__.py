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
    from neural_ai.core.system.factory import SystemComponentFactory
    from neural_ai.core.system.interfaces.health_interface import HealthMonitorInterface
    from neural_ai.core.utils.factory import HardwareFactory
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

    # DI container létrehozása
    container = DIContainer()

    # 1. Hardware inicializálása
    hardware = HardwareFactory.get_hardware_info()
    container.register_instance(HardwareInterface, hardware)

    # 2. Konfiguráció létrehozása
    config = ConfigManagerFactory.create_manager("yaml")
    # Betöltjük a configs/ mappát
    config.load_directory("configs")
    container.register_instance(ConfigManagerInterface, config)

    # 3. Logger inicializálása a konfiggal
    logging_config = config.get_section("logging") or {}
    LoggerFactory.configure(logging_config)
    # Alap logger példány létrehozása
    logger = LoggerFactory.get_logger(name="NeuralAI", logger_type="default")
    container.register_instance(LoggerInterface, logger)

    # 4. Adatbázis inicializálása (Config+Logger)
    # Helyesen a DatabaseFactory-t használjuk, és átadjuk a már betöltött configot
    database = DatabaseFactory.create_manager(config_manager=config)
    container.register_instance(DatabaseManager, database)

    # 5. EventBus inicializálása (Config+Logger)
    event_bus = EventBusFactory.create_from_config(config)
    container.register_instance(EventBusInterface, event_bus)

    # 6. Storage inicializálása (Config+Logger+HardwareInfo)
    storage_conf = config.get("storage") or {} # Szekció lekérése
    storage_type = storage_conf.get("type", "file") # Típus (file/parquet)

    storage = StorageFactory.get_storage(
        storage_type=storage_type,
        base_path=storage_conf.get("base_path"),
        logger=logger,
        hardware=hardware
    )
    container.register_instance(StorageInterface, storage)

    # 7. Rendszer monitorozás inicializálása
    health_monitor = SystemComponentFactory.create_health_monitor(
        name="core", logger=logger
    )
    container.register_instance(HealthMonitorInterface, health_monitor)

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
