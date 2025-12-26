"""Konfiguráció kezelő interfész."""

from abc import ABC, abstractmethod
from typing import Any


class ConfigManagerInterface(ABC):
    """Konfigurációkezelő interfész.

    Ez az interfész definiálja a konfigurációkezelők által implementálandó metódusokat.
    """

    @abstractmethod
    def __init__(self, filename: str | None = None) -> None:
        """Inicializálja a konfigurációkezelőt.

        Args:
            filename: Konfigurációs fájl útvonala (opcionális)
        """

    @abstractmethod
    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból."""

    @abstractmethod
    def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése."""

    @abstractmethod
    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban."""

    @abstractmethod
    def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése fájlba."""

    @abstractmethod
    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból."""

    @abstractmethod
    def load_directory(self, path: str) -> None:
        """Betölti az összes YAML fájlt egy mappából namespaced struktúrába.

        Args:
            path: A konfigurációs mappa útvonala
        """

    @abstractmethod
    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibák szótára)
        """
