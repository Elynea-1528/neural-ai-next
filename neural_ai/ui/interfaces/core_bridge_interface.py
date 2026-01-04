"""
Core Bridge interfész definíciója.

Ez az interfész definiálja a backend rendszerrel való kommunikációt
biztosító osztályok szerződését.
"""

from typing import Protocol, runtime_checkable, Any, Dict, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


@runtime_checkable
class CoreBridgeInterface(Protocol):
    """
    Core Bridge interfész - Backend kapcsolatért felelős.
    
    Ez az interfész definiálja a backend rendszerrel való kommunikációt
    biztosító metódusokat Singleton minta szerint.
    """

    def get_instance(self) -> "CoreBridgeInterface":
        """
        A Singleton példányt visszaadó metódus.
        
        Returns:
            CoreBridgeInterface: A Singleton példány
        """
        ...

    def initialize(self, config: Dict[str, Any], logger: "LoggerInterface") -> None:
        """
        A bridge inicializálása konfigurációval és loggerrel.
        
        Args:
            config: Konfigurációs beállítások
            logger: Logger példány
        """
        ...

    def get_component(self, component_type: str) -> Optional[Any]:
        """
        Komponens lekérése a backend rendszerből.
        
        Args:
            component_type: A lekérdezni kívánt komponens típusa
            
        Returns:
            Optional[Any]: A lekérdezett komponens vagy None
        """
        ...

    def send_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parancs küldése a backend rendszernek.
        
        Args:
            command: A végrehajtandó parancs
            params: A parancshoz tartozó paraméterek
            
        Returns:
            Dict[str, Any]: A parancs válasza
        """
        ...

    def get_system_info(self) -> Dict[str, Any]:
        """
        Rendszerinformáció lekérése a backendről.
        
        Returns:
            Dict[str, Any]: A rendszer aktuális állapotinformációi
        """
        ...

    @property
    def is_connected(self) -> bool:
        """
        A backendkel való kapcsolat állapotát ellenőrző property.
        
        Returns:
            bool: True, ha a kapcsolat aktív, egyébként False
        """
        ...