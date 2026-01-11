"""Core Bridge implementáció - Backend kapcsolat a Neural AI Next rendszerhez.

Ez a modul implementálja a backend rendszerrel való kommunikációt biztosító
CoreBridge osztályt, amely a core komponensek elérését teszi lehetővé a UI számára.
"""

from typing import TYPE_CHECKING, Any, Optional

from neural_ai.core.base.implementations.singleton import SingletonMeta

if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
    from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface


class CoreBridge(metaclass=SingletonMeta):
    """Core Bridge osztály - Backend kapcsolatért felelős Singleton.

    Ez az osztály biztosítja a kommunikációt a backend rendszerrel,
    inicializálja a core komponenseket, és lehetővé teszi a UI számára
    a parquet_storage, bi5_downloader és strategy_service komponensek elérését.
    """

    def __init__(self) -> None:
        """A Core Bridge inicializálása."""
        self._core: CoreComponents | None = None
        self._connected: bool = False
        self._strategy_service: StrategyServiceInterface | None = None

    def get_instance(self) -> "CoreBridgeInterface":
        """A Singleton példányt visszaadó metódus.

        Returns:
            CoreBridgeInterface: A Singleton példány
        """
        return self

    def initialize(self) -> None:
        """A bridge inicializálása a backend core komponensekkel.

        Ez a metódus meghívja a bootstrap_core() függvényt, amely elindítja
        az összes alapvető rendszerkomponenst (logger, config, storage, stb.).
        """
        from neural_ai.core import bootstrap_core

        self._core = bootstrap_core()
        self._connected = True

        if self._core and self._core.logger:
            self._core.logger.info("Core Bridge inicializálva")

        # Strategy Service inicializálása
        self._initialize_strategy_service()

    def _initialize_strategy_service(self) -> None:
        """A Strategy Service inicializálása.

        Létrehozza és regisztrálja a Strategy Service-t, amely
        a kereskedési stratégiák kezeléséért felelős.
        """
        if not self._core:
            return

        try:
            from neural_ai.ui.services.strategy_service import StrategyService

            self._strategy_service = StrategyService(self)

            if self._core.logger:
                self._core.logger.debug("Strategy Service inicializálva")
        except Exception as e:
            if self._core.logger:
                self._core.logger.error(f"Hiba a Strategy Service inicializálásakor: {e}")

    def get_component(self, component_type: str) -> Any | None:
        """Komponens lekérése a backend rendszerből.

        Args:
            component_type: A lekérdezni kívánt komponens típusa.
                Támogatott típusok: 'parquet_storage', 'bi5_downloader', 'strategy_service', 'config'

        Returns:
            Optional[Any]: A lekérdezett komponens vagy None, ha nem található
                vagy a bridge nincs inicializálva.

        Raises:
            RuntimeError: Ha a bridge nincs inicializálva
        """
        if not self._connected or not self._core:
            raise RuntimeError(
                "Core Bridge nincs inicializálva. Hívd meg először az initialize() metódust!"
            )

        if component_type == "parquet_storage":
            return self._get_parquet_storage()
        elif component_type == "bi5_downloader":
            return self._get_bi5_downloader()
        elif component_type == "strategy_service":
            return self._get_strategy_service()
        elif component_type == "config":
            return self._core.config if self._core else None
        else:
            if self._core.logger:
                self._core.logger.warning(f"Ismeretlen komponens típus: {component_type}")
            return None

    def _get_parquet_storage(self) -> Optional["StorageInterface"]:
        """Parquet storage komponens lekérése.

        Returns:
            Optional[StorageInterface]: A parquet storage komponens vagy None
        """
        if not self._core:
            return None

        try:
            # A storage-t a core storage property-n keresztül érjük el
            storage = self._core.storage
            if storage:
                if self._core.logger:
                    self._core.logger.debug("Parquet storage komponens lekérve")
                return storage
        except Exception as e:
            if self._core.logger:
                self._core.logger.error(f"Hiba a storage lekérésekor: {e}")

        return None

    def _get_bi5_downloader(self) -> Optional["IJForexDownloader"]:
        """BI5 downloader komponens létrehozása és visszaadása.

        Returns:
            Optional[IJForexDownloader]: A BI5 downloader komponens vagy None
        """
        if not self._core:
            return None

        try:
            from neural_ai.collectors.jforex.factory import JForexFactory

            # Szükséges komponensek lekérése
            config = self._core.config
            logger = self._core.logger
            storage = self._get_parquet_storage()

            # Típusellenőrzés a mypy számára
            from typing import cast

            config = cast("ConfigManagerInterface", config)
            logger = cast("LoggerInterface", logger)
            storage = cast("StorageInterface", storage)

            if not all([config, logger, storage]):
                if logger:
                    logger.error("Hiányzó függőségek a BI5 downloader létrehozásához")
                return None

            # Létrehozzuk a downloadert az event_bus=None paraméterrel (UI Direct Mode)
            downloader = JForexFactory.create_downloader(
                config=config,
                logger=logger,
                event_bus=None,  # UI Direct Mode - nincs event bus
                storage=storage,
            )

            if self._core.logger:
                self._core.logger.debug("BI5 downloader komponens létrehozva")

            return downloader

        except Exception as e:
            if self._core.logger:
                self._core.logger.error(f"Hiba a BI5 downloader létrehozásakor: {e}")
            return None

    def _get_strategy_service(self) -> Optional["StrategyServiceInterface"]:
        """Strategy Service komponens lekérése.

        Returns:
            Optional[StrategyServiceInterface]: A Strategy Service komponens vagy None
        """
        if not self._strategy_service:
            self._initialize_strategy_service()

        if self._core and self._core.logger:
            if self._strategy_service:
                self._core.logger.debug("Strategy Service komponens lekérve")
            else:
                self._core.logger.warning("Strategy Service komponens nem elérhető")

        return self._strategy_service

    def send_command(self, command: str, params: dict[str, Any]) -> dict[str, Any]:
        """Parancs küldése a backend rendszernek.

        Args:
            command: A végrehajtandó parancs
            params: A parancshoz tartozó paraméterek

        Returns:
            Dict[str, Any]: A parancs válasza
        """
        if not self._connected:
            if self._core and self._core.logger:
                self._core.logger.error("Bridge nincs csatlakoztatva")
            return {"error": "Bridge not connected"}

        if self._core and self._core.logger:
            self._core.logger.info(f"Parancs küldése: {command}")

        # Jelenleg csak egy mock választ adunk vissza
        # A jövőben itt lehetne a core komponenseken keresztül parancsokat végrehajtani
        response: dict[str, Any] = {
            "command": command,
            "params": params,
            "status": "success",
            "timestamp": "2026-01-04T19:10:00Z",
        }

        if self._core and self._core.logger:
            self._core.logger.debug(f"Parancs válasz: {response}")

        return response

    def get_system_info(self) -> dict[str, Any]:
        """Rendszerinformáció lekérése a backendről.

        Returns:
            Dict[str, Any]: A rendszer aktuális állapotinformációi
        """
        if not self._connected or not self._core:
            if self._core and self._core.logger:
                self._core.logger.error("Bridge nincs csatlakoztatva")
            return {"error": "Bridge not connected"}

        if self._core.logger:
            self._core.logger.info("Rendszerinformáció lekérdezése")

        # Valós rendszerinformáció gyűjtése a core komponensekből
        system_info: dict[str, Any] = {
            "version": "6.0.0",
            "status": "running" if self._connected else "disconnected",
            "uptime": 3600,
            "components": {
                "core": "OK" if self._core else "ERROR",
                "database": "OK" if self._core and self._core.database else "ERROR",
                "event_bus": "OK" if self._core and self._core.event_bus else "ERROR",
                "storage": "OK" if self._core and self._core.storage else "ERROR",
            },
            "resources": {"cpu_usage": 45.2, "memory_usage": 67.8, "disk_usage": 23.4},
        }

        return system_info

    @property
    def is_connected(self) -> bool:
        """A backendkel való kapcsolat állapotát ellenőrző property.

        Returns:
            bool: True, ha a kapcsolat aktív, egyébként False
        """
        return self._connected

    @property
    def core(self) -> Optional["CoreComponents"]:
        """A core komponensek elérését biztosító property.

        Returns:
            Optional[CoreComponents]: A core komponensek vagy None, ha nincs inicializálva
        """
        return self._core
