"""Data Service interfész definíciója.

Ez az interfész definiálja az adatkezelési szolgáltatás szerződését,
amely az adatok betöltését, szűrését és kezelését végzi.
"""

from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import pandas as pd

if TYPE_CHECKING:
    pass


@runtime_checkable
class DataServiceInterface(Protocol):
    """Data Service interfész - Adatkezelésért felelős.

    Ez az interfész definiálja az adatok lekérdezését és kezelését
    végző metódusokat, Big Data támogatással.
    """

    def load_data(
        self, source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000
    ) -> Generator[list[dict[str, Any]], None, None]:
        """Adatok aszinkron betöltése chunkokban.

        Args:
            source: Az adatforrás azonosítója
            filters: Szűrőfeltételek
            chunk_size: A chunkok mérete

        Yields:
            List[Dict[str, Any]]: Adat chunkok
        """
        ...

    def get_data_sources(self) -> list[dict[str, str]]:
        """Elérhető adatforrások lekérdezése.

        Returns:
            List[Dict[str, str]]: Az adatforrások listája
        """
        ...

    def get_data_info(self, source: str) -> dict[str, Any]:
        """Adatforrás információk lekérdezése.

        Args:
            source: Az adatforrás azonosítója

        Returns:
            Dict[str, Any]: Az adatforrás metaadatai
        """
        ...

    def apply_filters(
        self, data: list[dict[str, Any]], filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Szűrők alkalmazása adatokra.

        Args:
            data: A szűrendő adatok
            filters: A alkalmazandó szűrők

        Returns:
            List[Dict[str, Any]]: A szűrt adatok
        """
        ...

    def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool:
        """Adatok exportálása különböző formátumokba.

        Args:
            data: Az exportálandó adatok
            format: A célformátum (parquet, csv, json)
            destination: A cél útvonal

        Returns:
            bool: True, ha sikeres az exportálás
        """
        ...

    def get_default_date_range(self) -> tuple[datetime, datetime]:
        """Alapértelmezett dátumtartomány lekérdezése a konfigurációból.

        A metódus kiolvassa a configból a dátumokat, és datetime objektumokká
        konvertálja őket. Ha a konfiguráció üres vagy hiba történik, akkor
        fallback értékeket használ.

        Returns:
            tuple[datetime, datetime]: A kezdő és záró dátum tuple-ben.
                Fallback: (2020-01-01, ma)
        """
        ...

    async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]:
        """Történelmi adatok letöltése aszinkron módon a Data Hub-ból.

        Args:
            symbol: A szimbólum (pl. 'EURUSD' vagy 'ALL' az összesre)
            start: A kezdő dátum
            end: A záró dátum

        Returns:
            Dict[str, Any]: A letöltés eredménye és metaadatok
        """
        ...

    def list_available_data(self, symbol: str | None = None) -> pd.DataFrame:
        """Elérhető adatok listázása a Data Hub-ban.

        Args:
            symbol: Opcionális szimbólum szűréshez

        Returns:
            pd.DataFrame: Az elérhető adatok táblázata
        """
        ...

    def get_storage_path(self) -> Path:
        """A Data Hub tárhelyének elérési útjának lekérdezése.

        Returns:
            Path: A tárhely elérési útja
        """
        ...

    def get_configured_symbols(self) -> list[str]:
        """Konfigurált szimbólumok lekérdezése.

        A metódus a konfigurációból kiolvassa a JForex collectorhoz tartozó
        szimbólumokat. Ha a konfiguráció üres vagy hiba történik, akkor
        egy alapértelmezett szimbólumlistát ad vissza.

        Returns:
            list[str]: A konfigurált szimbólumok listája. Alapértelmezett
                esetben ["EURUSD"]-t ad vissza.
        """
        ...
