"""Konfiguráció kezelő interfész."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class ConfigManagerInterface(ABC):
    """Konfigurációkezelő interfész.

    Ez az interfész definiálja a konfigurációkezelők által implementálandó metódusokat.
    """

    @abstractmethod
    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból."""

    @abstractmethod
    def get_section(self, section: str) -> Dict[str, Any]:
        """Teljes konfigurációs szekció lekérése."""

    @abstractmethod
    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban."""

    @abstractmethod
    def save(self, filename: Optional[str] = None) -> None:
        """Konfiguráció mentése fájlba."""

    @abstractmethod
    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból."""

    @abstractmethod
    def validate(self, schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibák szótára)
        """
