"""Konfiguráció kezelő interfészek.

Ez a modul tartalmazza a konfigurációkezelő interfész definícióját.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class ConfigManagerInterface(ABC):
    """Alap interfész a konfigurációkezelő implementációkhoz.

    Ez az interfész definiálja azokat a műveleteket, amelyeket minden
    konfigurációkezelő implementációnak támogatnia kell.
    """

    @abstractmethod
    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból.

        Args:
            *keys: Kulcs útvonal (pl. "database", "host")
            default: Alapértelmezett érték, ha a kulcs nem létezik

        Returns:
            Any: A kért konfigurációs érték vagy az alapértelmezett érték
        """
        pass

    @abstractmethod
    def get_section(self, section: str) -> Dict[str, Any]:
        """Teljes konfigurációs szekció lekérése.

        Args:
            section: A szekció neve

        Returns:
            Dict[str, Any]: A szekció összes beállítása

        Raises:
            KeyError: Ha a szekció nem létezik
        """
        pass

    @abstractmethod
    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban.

        Args:
            *keys: Kulcs útvonal (pl. "database", "host")
            value: Az új érték

        Raises:
            ValueError: Ha a kulcs útvonal érvénytelen
        """
        pass

    @abstractmethod
    def save(self, filename: Optional[str] = None) -> None:
        """Aktuális konfiguráció mentése fájlba.

        Args:
            filename: Opcionális fájlnév. Ha nincs megadva,
                     az eredeti fájlba ment

        Raises:
            IOError: Ha a mentés sikertelen
        """
        pass

    @abstractmethod
    def validate(self, schema: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: Validációs séma

        Returns:
            Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibaüzenetek)
        """
        pass

    @abstractmethod
    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból.

        Args:
            filename: A betöltendő fájl neve

        Raises:
            FileNotFoundError: Ha a fájl nem létezik
            ValueError: Ha a fájl formátuma érvénytelen
        """
        pass
