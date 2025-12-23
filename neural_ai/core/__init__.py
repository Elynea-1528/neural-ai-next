"""Neural-AI-Next core komponensek inicializációs modul.

Ez a modul a rendszer alapvető infrastrukturális komponenseit tartalmazza:
- Logger rendszer
- Konfiguráció kezelés
- Adattárolás

A modul biztosítja a core komponensek megfelelő inicializálását és
függőségi injektálását, elkerülve a körkörös függőségeket.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


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


class CoreComponents:
    """Core komponensek tároló osztálya.

    Ez az osztály tárolja a rendszer alapvető komponenseit, biztosítva
    a hozzáférésüket az egész alkalmazásban.

    Attributes:
        config: A konfiguráció kezelő interfész
        logger: A logger interfész
        storage: A tárhely kezelő interfész
    """

    def __init__(
        self,
        config: "ConfigManagerInterface",
        logger: "LoggerInterface",
        storage: "StorageInterface",
    ) -> None:
        """Inicializálja a core komponenseket.

        Args:
            config: A konfiguráció kezelő példány
            logger: A logger példány
            storage: A tárhely kezelő példány
        """
        self.config: ConfigManagerInterface = config
        self.logger: LoggerInterface = logger
        self.storage: StorageInterface = storage


def bootstrap_core(config_path: str | None = None, log_level: str | None = None) -> CoreComponents:
    """Bootstrap funkció a core komponensek inicializálásához.

    Ez a függvény biztosítja a core komponensek megfelelő sorrendű
    inicializálását, elkerülve a körkörös függőségeket.

    A bootstrap folyamat:
    1. Alap konfiguráció létrehozása
    2. Logger inicializálása a konfiggal
    3. Konfig frissítése a valódi loggerrel
    4. Storage inicializálása

    Args:
        config_path: Opcionális konfigurációs fájl útvonala
        log_level: Opcionális log szint beállítás

    Returns:
        A teljesen inicializált CoreComponents példány

    Example:
        >>> core = bootstrap_core()
        >>> core.logger.info("Alkalmazás elindult")
        >>> config_value = core.config.get("database.host")
    """
    # Importok a függőségi körkörök elkerüléséhez
    from neural_ai.core.config.implementations.config_manager_factory import ConfigManagerFactory
    from neural_ai.core.logger.implementations.logger_factory import LoggerFactory
    from neural_ai.core.storage.implementations.storage_factory import StorageFactory

    # 1. Konfiguráció létrehozása
    config = ConfigManagerFactory.get_manager(filename=config_path or "config.yml")

    # 2. Logger létrehozása a konfiggal
    logger = LoggerFactory.get_logger(name="NeuralAI", logger_type="default", level=log_level)

    # 3. Storage inicializálása
    storage = StorageFactory.get_storage(storage_type="file", base_path=None, logger=logger)

    return CoreComponents(config=config, logger=logger, storage=storage)


def get_core_components() -> CoreComponents:
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
    "CoreComponents",
    "bootstrap_core",
    "get_core_components",
    "get_version",
    "get_schema_version",
]
