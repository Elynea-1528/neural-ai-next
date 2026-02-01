"""UI Main Application - A felhasználói felület fő alkalmazása.

Ez a modul implementálja a UI alkalmazás fő belépési pontját,
amely összekapcsolja az összes UI komponenst.
"""

from typing import TYPE_CHECKING, Any, Optional, cast

from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.ui.factory import UIFactoryConfig, UIServiceFactory

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface


class UIApplication:
    """UI Application - A felhasználói felület fő alkalmazása.

    Ez az osztály felelős a teljes UI rendszer inicializálásáért és
    működtetéséért, összekapcsolva az összes komponenst.
    """

    def __init__(
        self, config: dict[str, Any] | None = None, logger: Optional["LoggerInterface"] = None
    ) -> None:
        """A UI alkalmazás inicializálása.

        Args:
            config: Konfigurációs beállítások
            logger: Logger példány
        """
        self._config = config or {}
        self._logger = logger
        self._bridge: CoreBridge | None = None
        self._factory: UIServiceFactory | None = None
        self._navigation: NavigationServiceInterface | None = None
        self._core_components: Any = None
        self._running: bool = False
        self._init_error: Exception | None = None

    def initialize(self) -> bool:
        """Az alkalmazás inicializálása.

        Returns:
            bool: True, ha sikeres az inicializálás
        """
        try:
            if self._logger:
                self._logger.info("UI alkalmazás inicializálása...")

            # Core Bridge létrehozása és inicializálása
            self._bridge = CoreBridge()
            self._bridge.initialize()

            # Core components wrapper (a bridge tartalmazza a core komponenseket)
            self._core_components = self._bridge

            # UI config létrehozása TypedDict szerint
            ui_config = cast(UIFactoryConfig, self._config.get("ui", {}))

            # UI Service Factory létrehozása és inicializálása
            self._factory = UIServiceFactory()
            self._factory.initialize(
                bridge=self._bridge,
                config=ui_config,
                logger=self._logger,
                core_components=self._core_components,
            )

            # Navigation Service lekérése (paraméterek nélkül - factory használja a tárolt értékeket)
            self._navigation = self._factory.get_navigation_service()

            if self._logger:
                self._logger.info("UI alkalmazás inicializálva")

            return True

        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba az inicializálás során: {e}")
            self._init_error = e
            return False

    def run(self) -> None:
        """Az alkalmazás indítása."""
        if not self._factory or not self._navigation:
            raise RuntimeError("Alkalmazás nincs inicializálva")

        self._running = True

        if self._logger:
            self._logger.info("UI alkalmazás elindítva")

        # Itt valós implementációban a fő UI ciklus futna
        # Most csak szimuláljuk
        print("UI alkalmazás fut...")

    def stop(self) -> None:
        """Az alkalmazás leállítása."""
        self._running = False

        if self._logger:
            self._logger.info("UI alkalmazás leállítva")

        print("UI alkalmazás leállítva")

    def get_navigation_service(self) -> "NavigationServiceInterface":
        """Navigation Service lekérdezése.

        Returns:
            NavigationServiceInterface: A Navigation Service példány
        """
        if not self._navigation:
            raise RuntimeError("Alkalmazás nincs inicializálva")

        return self._navigation

    def get_factory(self) -> UIServiceFactory:
        """UI Service Factory lekérdezése.

        Returns:
            UIServiceInterface: Az UI Service Factory példány
        """
        if not self._factory:
            raise RuntimeError("Alkalmazás nincs inicializálva")

        return self._factory

    @property
    def is_running(self) -> bool:
        """Az alkalmazás futási állapotát ellenőrző property.

        Returns:
            bool: True, ha az alkalmazás fut, egyébként False
        """
        return self._running

    @is_running.setter
    def is_running(self, value: bool) -> None:
        """Az alkalmazás futási állapotának beállítása.

        Args:
            value: Az új futási állapot
        """
        self._running = value

    @property
    def is_initialized(self) -> bool:
        """Az alkalmazás inicializáltságát ellenőrző property.

        Returns:
            bool: True, ha az alkalmazás inicializálva van, egyébként False
        """
        return self._factory is not None and self._navigation is not None

    @property
    def init_error(self) -> Exception | None:
        """Az inicializálási hiba lekérdezése.

        Returns:
            Exception | None: A hiba, ha volt, egyébként None
        """
        return self._init_error

    @property
    def config(self) -> dict[str, Any]:
        """Konfigurációs beállítások lekérdezése.

        Returns:
            dict[str, Any]: A konfigurációs szótár
        """
        return self._config

    @config.setter
    def config(self, value: dict[str, Any]) -> None:
        """Konfigurációs beállítások beállítása.

        Args:
            value: Az új konfigurációs szótár
        """
        self._config = value

    @property
    def logger(self) -> Optional["LoggerInterface"]:
        """Logger példány lekérdezése.

        Returns:
            LoggerInterface | None: A logger példány, vagy None
        """
        return self._logger

    @logger.setter
    def logger(self, value: Optional["LoggerInterface"]) -> None:
        """Logger példány beállítása.

        Args:
            value: Az új logger példány
        """
        self._logger = value

    @property
    def bridge(self) -> CoreBridge | None:
        """Core Bridge példány lekérdezése.

        Returns:
            CoreBridge | None: A bridge példány, vagy None
        """
        return self._bridge

    @bridge.setter
    def bridge(self, value: CoreBridge | None) -> None:
        """Core Bridge példány beállítása.

        Args:
            value: Az új bridge példány
        """
        self._bridge = value

    @property
    def factory(self) -> UIServiceFactory | None:
        """UI Service Factory példány lekérdezése.

        Returns:
            UIServiceFactory | None: A factory példány, vagy None
        """
        return self._factory

    @factory.setter
    def factory(self, value: UIServiceFactory | None) -> None:
        """UI Service Factory példány beállítása.

        Args:
            value: Az új factory példány
        """
        self._factory = value

    @property
    def navigation(self) -> Optional["NavigationServiceInterface"]:
        """Navigation Service példány lekérdezése.

        Returns:
            NavigationServiceInterface | None: A navigation példány, vagy None
        """
        return self._navigation

    @navigation.setter
    def navigation(self, value: Optional["NavigationServiceInterface"]) -> None:
        """Navigation Service példány beállítása.

        Args:
            value: Az új navigation példány
        """
        self._navigation = value
