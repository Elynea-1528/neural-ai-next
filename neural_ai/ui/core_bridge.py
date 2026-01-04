"""
Core Bridge implementáció - Singleton backend kapcsolat.

Ez a modul implementálja a backend rendszerrel való kommunikációt
biztosító osztályt Singleton minta szerint.
"""

from typing import Dict, Any, Optional, TYPE_CHECKING
from neural_ai.core.base.implementations.singleton import SingletonMeta

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class CoreBridge(metaclass=SingletonMeta):
    """
    Core Bridge osztály - Backend kapcsolatért felelős Singleton.
    
    Ez az osztály biztosítja a kommunikációt a backend rendszerrel,
    és garantálja, hogy csak egy példány létezzen belőle.
    """

    def __init__(self) -> None:
        """A Core Bridge inicializálása."""
        self._config: Optional[Dict[str, Any]] = None
        self._logger: Optional["LoggerInterface"] = None
        self._connected: bool = False
        self._components: Dict[str, Any] = {}

    def get_instance(self) -> "CoreBridge":
        """
        A Singleton példányt visszaadó metódus.
        
        Returns:
            CoreBridge: A Singleton példány
        """
        return self

    def initialize(
        self,
        config: Dict[str, Any],
        logger: "LoggerInterface"
    ) -> None:
        """
        A bridge inicializálása konfigurációval és loggerrel.
        
        Args:
            config: Konfigurációs beállítások
            logger: Logger példány
        """
        self._config = config
        self._logger = logger
        self._connected = True
        
        if self._logger:
            self._logger.info("Core Bridge inicializálva")

    def get_component(self, component_type: str) -> Optional[Any]:
        """
        Komponens lekérése a backend rendszerből.
        
        Args:
            component_type: A lekérdezni kívánt komponens típusa
            
        Returns:
            Optional[Any]: A lekérdezett komponens vagy None
        """
        if not self._connected:
            if self._logger:
                self._logger.warning("Bridge nincs csatlakoztatva")
            return None

        # Itt valós implementációban a backend API-t hívnánk meg
        component = self._components.get(component_type)
        
        if self._logger:
            if component:
                self._logger.debug(f"Komponens lekérve: {component_type}")
            else:
                self._logger.warning(f"Komponens nem található: {component_type}")
        
        return component

    def send_command(
        self,
        command: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parancs küldése a backend rendszernek.
        
        Args:
            command: A végrehajtandó parancs
            params: A parancshoz tartozó paraméterek
            
        Returns:
            Dict[str, Any]: A parancs válasza
        """
        if not self._connected:
            if self._logger:
                self._logger.error("Bridge nincs csatlakoztatva")
            return {"error": "Bridge not connected"}

        if self._logger:
            self._logger.info(f"Parancs küldése: {command}")

        # Itt valós implementációban a backend API-t hívnánk meg
        # Most csak egy mock választ adunk vissza
        response = {
            "command": command,
            "params": params,
            "status": "success",
            "timestamp": "2026-01-04T19:10:00Z"
        }

        if self._logger:
            self._logger.debug(f"Parancs válasz: {response}")

        return response

    def get_system_info(self) -> Dict[str, Any]:
        """
        Rendszerinformáció lekérése a backendről.
        
        Returns:
            Dict[str, Any]: A rendszer aktuális állapotinformációi
        """
        if not self._connected:
            if self._logger:
                self._logger.error("Bridge nincs csatlakoztatva")
            return {"error": "Bridge not connected"}

        if self._logger:
            self._logger.info("Rendszerinformáció lekérdezése")

        # Mock rendszerinformáció
        system_info = {
            "version": "6.0.0",
            "status": "running",
            "uptime": 3600,
            "components": {
                "core": "OK",
                "database": "OK",
                "event_bus": "OK"
            },
            "resources": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.4
            }
        }

        return system_info

    @property
    def is_connected(self) -> bool:
        """
        A backendkel való kapcsolat állapotát ellenőrző property.
        
        Returns:
            bool: True, ha a kapcsolat aktív, egyébként False
        """
        return self._connected

    def _register_component(self, component_type: str, component: Any) -> None:
        """
        Belső metódus komponens regisztrálására (teszteléshez).
        
        Args:
            component_type: A komponens típusa
            component: A komponens példány
        """
        self._components[component_type] = component
        if self._logger:
            self._logger.debug(f"Komponens regisztrálva: {component_type}")