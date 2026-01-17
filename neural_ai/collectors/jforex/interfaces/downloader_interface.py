"""JForex Downloader Interface Definition."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.tick_data import TickData


class IJForexDownloader(ABC):
    """JForex .bi5 adat letöltő interfész.

    Ez az interfész definiálja a szerződést a Dukascopy natív .bi5 tick adat
    formátum letöltéséhez és feldolgozásához.
    """

    @abstractmethod
    async def download_tick_data(self, symbol: str, date: datetime) -> list["TickData"]:
        """Tick adatok letöltése és dekódolása adott szimbólumhoz és dátumhoz.

        Args:
            symbol: Kereskedelmi szimbólum (pl. 'EURUSD', 'GBPUSD')
            date: Dátum, amelyhez az adatokat le kell tölteni

        Returns:
            TickData objektumok listája bid/ask árakkal

        Raises:
            DownloadError: Ha a letöltés sikertelen (hálózati problémák, szerverhibák)
            DecodeError: Ha az adat dekódolása sikertelen (sérült fájl)
            DataNotAvailableError: Ha az adat nem elérhető (hétvége, ünnep)
        """
        pass

    @abstractmethod
    async def get_available_dates(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> list[datetime]:
        """Szimbólum elérhető adatainak dátumlistája.

        Args:
            symbol: Kereskedelmi szimbólum
            start_date: Dátumtartomány kezdete
            end_date: Dátumtartomány vége

        Returns:
            Elérhető adatokkal rendelkező dátumok datetime objektumai
        """
        pass

    @abstractmethod
    def validate_bi5_data(self, data: bytes) -> bool:
        """.bi5 adat integritásának ellenőrzése.

        Args:
            data: Nyers .bi5 adat bájtok

        Returns:
            True ha az adat érvényes, különben False
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Letöltő bezárása és erőforrások felszabadítása.

        Ez a metódus biztosítja, hogy minden hálózati kapcsolat megfelelően
        bezáródjon és az erőforrások felszabaduljanak, amikor a letöltőre már nincs szükség.
        """
        pass
