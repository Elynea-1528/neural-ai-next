"""Aszinkron konfiguráció kezelő interfész.

Ez az interfész definiálja az aszinkron konfigurációkezelők által implementálandó metódusokat,
különösen az adatbázis-alapú dinamikus konfigurációkezelőkhöz.
"""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any


# Type alias a konfiguráció változásokat figyelő callback-ekhez
ConfigListener = Callable[[str, Any], Awaitable[None]]


class AsyncConfigManagerInterface(ABC):
    """Aszinkron konfigurációkezelő interfész.

    Ez az interfész definiálja az aszinkron konfigurációkezelők által implementálandó metódusokat,
    amelyek főleg adatbázis-alapú dinamikus konfigurációkezelésre szolgálnak.
    """

    @abstractmethod
    async def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája.
            default: Alapértelmezett érték, ha a kulcs nem található.

        Returns:
            A konfigurációs érték vagy az alapértelmezett érték.
        """

    @abstractmethod
    async def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése.

        Args:
            section: A konfigurációs szekció/kategória neve.

        Returns:
            A szekció konfigurációs adatai.

        Raises:
            KeyError: Ha a szekció nem található.
        """

    @abstractmethod
    async def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban.

        Args:
            *keys: A konfigurációs kulcs(ok) hierarchiája.
            value: A beállítandó érték.

        Raises:
            ValueError: Ha érvénytelen a kulcs vagy érték.
        """

    @abstractmethod
    async def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése.

        Args:
            filename: A mentési cél (opcionális, implementációfüggő).

        Raises:
            NotImplementedError: Ha a művelet nem támogatott.
        """

    @abstractmethod
    async def load(self, filename: str) -> None:
        """Konfiguráció betöltése.

        Args:
            filename: A betöltési forrás.

        Raises:
            NotImplementedError: Ha a művelet nem támogatott.
        """

    @abstractmethod
    async def load_directory(self, path: str) -> None:
        """Betölti az összes konfigurációs fájlt egy mappából.

        Args:
            path: A konfigurációs mappa útvonala.

        Raises:
            NotImplementedError: Ha a művelet nem támogatott.
        """

    @abstractmethod
    async def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján.

        Args:
            schema: A validáláshoz használt séma.

        Returns:
            Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)
        """

    @abstractmethod
    def add_listener(self, callback: ConfigListener) -> None:
        """Listener hozzáadása konfiguráció változásokhoz.

        Args:
            callback: A callback függvény, amelyet hívni kell a változás esetén.
        """

    @abstractmethod
    def remove_listener(self, callback: ConfigListener) -> None:
        """Listener eltávolítása.

        Args:
            callback: Az eltávolítandó callback függvény.
        """

    @abstractmethod
    async def start_hot_reload(self, interval: float = 5.0) -> None:
        """Hot reload indítása (háttérben fut).

        Args:
            interval: Az ellenőrzési időköz másodpercben.

        Raises:
            RuntimeError: Ha a hot reload már fut.
        """

    @abstractmethod
    async def stop_hot_reload(self) -> None:
        """Hot reload leállítása."""

    @abstractmethod
    async def get_all(self, category: str | None = None) -> dict[str, Any]:
        """Összes konfiguráció lekérdezése.

        Args:
            category: Opcionális kategória szűréshez.

        Returns:
            Szótár az összes (vagy kategóriához tartozó) konfigurációval.
        """

    @abstractmethod
    async def set_with_metadata(
        self,
        key: str,
        value: Any,
        category: str = "system",
        description: str | None = None,
        is_active: bool = True,
    ) -> None:
        """Konfiguráció beállítása metaadatokkal.

        Args:
            key: A konfigurációs kulcs.
            value: A konfigurációs érték.
            category: A konfiguráció kategóriája.
            description: A konfiguráció leírása.
            is_active: A konfiguráció aktív-e.
        """

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Konfiguráció törlése (soft delete).

        Args:
            key: A törlendő konfigurációs kulcs.

        Returns:
            True ha a konfiguráció törölve lett, False ha nem található.
        """