"""
Interfész sablon a Neural-AI-Next projekthez.

Ez a fájl egy általános interfész sablont tartalmaz,
amelyet új komponens interfészek definiálásához lehet használni.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union  # noqa: F401 - Sablon részeként szerepel


class ComponentInterface(ABC):
    """
    Komponens interfész leírása.

    Ez az interfész definiálja egy komponens által nyújtott
    alapvető funkcionalitást és API-t.
    """

    @abstractmethod
    def main_operation(self, input_data: Any) -> Any:
        """
        Fő művelet leírása.

        Args:
            input_data: Bemeneti adatok

        Returns:
            Kimeneti adatok

        Raises:
            ComponentException: Feldolgozási hiba esetén
        """
        pass

    @abstractmethod
    def get_configuration(self) -> Dict[str, Any]:
        """
        Komponens konfigurációjának lekérése.

        Returns:
            A komponens aktuális konfigurációja
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Komponens állapotának lekérése.

        Returns:
            A komponens aktuális állapota
        """
        pass


class ComponentFactoryInterface(ABC):
    """
    Komponens factory interfész.

    Ez az interfész definiálja a komponens példányokat létrehozó
    factory objektumok közös API-ját.
    """

    @staticmethod
    @abstractmethod
    def create_component(config: Dict[str, Any], logger=None) -> ComponentInterface:
        """
        Komponens példány létrehozása.

        Args:
            config: Komponens konfiguráció
            logger: Opcionális logger példány

        Returns:
            ComponentInterface: Új komponens példány

        Raises:
            ValueError: Érvénytelen konfiguráció esetén
        """
        pass

    @staticmethod
    @abstractmethod
    def get_component_types() -> List[str]:
        """
        Elérhető komponens típusok lekérése.

        Returns:
            A factory által támogatott komponens típusok listája
        """
        pass


class ComponentException(Exception):
    """
    Komponens specifikus kivétel.

    Az interfészt implementáló komponensek által dobott kivétel.
    """

    pass


class InterfaceTemplate(ABC):
    """Alap interfész template."""

    @abstractmethod
    def method1(self) -> None:
        """
        Első absztrakt metódus.
        """
        pass

    @abstractmethod
    def method2(self, param1: str) -> Dict[str, Any]:
        """
        Második absztrakt metódus.

        Args:
            param1: Első paraméter

        Returns:
            Dict[str, Any]: Visszatérési érték
        """
        pass
