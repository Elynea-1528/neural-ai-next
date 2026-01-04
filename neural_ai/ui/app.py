"""
UI Main Application - A felhasználói felület fő alkalmazása.

Ez a modul implementálja a UI alkalmazás fő belépési pontját,
amely összekapcsolja az összes UI komponenst.
"""

from typing import Dict, Any, Optional, TYPE_CHECKING

from neural_ai.ui.core_bridge import CoreBridge
from neural_ai.ui.factory import UIServiceFactory

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface


class UIApplication:
    """
    UI Application - A felhasználói felület fő alkalmazása.
    
    Ez az osztály felelős a teljes UI rendszer inicializálásáért és
    működtetéséért, összekapcsolva az összes komponenst.
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        logger: Optional["LoggerInterface"] = None
    ) -> None:
        """
        A UI alkalmazás inicializálása.
        
        Args:
            config: Konfigurációs beállítások
            logger: Logger példány
        """
        self._config = config or {}
        self._logger = logger
        self._bridge: Optional[CoreBridge] = None
        self._factory: Optional[UIServiceFactory] = None
        self._navigation: Optional[NavigationServiceInterface] = None
        self._running: bool = False

    def initialize(self) -> bool:
        """
        Az alkalmazás inicializálása.
        
        Returns:
            bool: True, ha sikeres az inicializálás
        """
        try:
            if self._logger:
                self._logger.info("UI alkalmazás inicializálása...")

            # Core Bridge létrehozása és inicializálása
            self._bridge = CoreBridge()
            if self._logger:
                self._bridge.initialize(self._config, self._logger)
            else:
                self._bridge.initialize(self._config, None)

            # UI Service Factory létrehozása és inicializálása
            self._factory = UIServiceFactory()
            self._factory.initialize(self._bridge)

            # Navigation Service lekérése
            self._navigation = self._factory.get_navigation_service()

            if self._logger:
                self._logger.info("UI alkalmazás inicializálva")

            return True

        except Exception as e:
            if self._logger:
                self._logger.error(f"Hiba az inicializálás során: {e}")
            return False

    def run(self) -> None:
        """
        Az alkalmazás indítása.
        """
        if not self._factory or not self._navigation:
            raise RuntimeError("Alkalmazás nincs inicializálva")

        self._running = True

        if self._logger:
            self._logger.info("UI alkalmazás elindítva")

        # Itt valós implementációban a fő UI ciklus futna
        # Most csak szimuláljuk
        print("UI alkalmazás fut...")

    def stop(self) -> None:
        """
        Az alkalmazás leállítása.
        """
        self._running = False

        if self._logger:
            self._logger.info("UI alkalmazás leállítva")

        print("UI alkalmazás leállítva")

    def get_navigation_service(self) -> NavigationServiceInterface:
        """
        Navigation Service lekérdezése.
        
        Returns:
            NavigationServiceInterface: A Navigation Service példány
        """
        if not self._navigation:
            raise RuntimeError("Alkalmazás nincs inicializálva")

        return self._navigation

    def get_factory(self) -> UIServiceFactory:
        """
        UI Service Factory lekérdezése.
        
        Returns:
            UIServiceInterface: Az UI Service Factory példány
        """
        if not self._factory:
            raise RuntimeError("Alkalmazás nincs inicializálva")

        return self._factory

    @property
    def is_running(self) -> bool:
        """
        Az alkalmazás futási állapotát ellenőrző property.
        
        Returns:
            bool: True, ha az alkalmazás fut, egyébként False
        """
        return self._running

    @property
    def is_initialized(self) -> bool:
        """
        Az alkalmazás inicializáltságát ellenőrző property.
        
        Returns:
            bool: True, ha az alkalmazás inicializálva van, egyébként False
        """
        return self._factory is not None and self._navigation is not None