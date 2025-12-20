"""MT5 Collector interfész definíció.

Ez a modul tartalmazza az MT5 Collector komponens interfészét,
amelyet minden implementációnak implementálnia kell.

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

import datetime as dt
from abc import ABC, abstractmethod

import pandas as pd


class CollectorInterface(ABC):
    """MT5 Collector interfész.

    Definíciója az MT5 platformról történő adatgyűjtés
    alapvető műveleteinek.
    """

    @abstractmethod
    async def connect(self) -> bool:
        """Kapcsolódás az MT5 platformhoz.

        Returns:
            True sikeres kapcsolódás esetén, egyébként False

        Raises:
            ConnectionError: Kapcsolódási hiba esetén
        """
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Kapcsolat bontása.

        Returns:
            True sikeres kapcsolatbontás esetén
        """
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Kapcsolat állapotának ellenőrzése.

        Returns:
            True ha kapcsolódva van, egyébként False
        """
        pass

    @abstractmethod
    async def collect_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None = None,
        end_date: str | dt.datetime | None = None,
    ) -> pd.DataFrame:
        """Adatok gyűjtése.

        Args:
            symbol: Szimbólum (pl. "EURUSD")
            timeframe: Időkeret (pl. "M1", "H1")
            start_date: Kezdő dátum
            end_date: Záró dátum

        Returns:
            Gyűjtött adatok DataFrame-ben

        Raises:
            DataFetchError: Adatlekérési hiba esetén
            ValidationError: Validációs hiba esetén
        """
        pass

    @abstractmethod
    async def get_available_symbols(self) -> list[str]:
        """Elérhető szimbólumok lekérése.

        Returns:
            Szimbólumok listája
        """
        pass

    @abstractmethod
    def get_available_timeframes(self) -> dict[str, int]:
        """Elérhető időkeretek lekérése.

        Returns:
            Időkeretek szótára
        """
        pass
