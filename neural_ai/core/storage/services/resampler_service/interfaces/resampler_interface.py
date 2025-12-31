"""ResamplerService Interface - Tick adatokból OHLCV gyertyák létrehozásáért felelős."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


class ResamplerInterface(ABC):
    """ResamplerService interfész, amely definiálja a tick adatok OHLCV gyertyákká alakítását."""

    @abstractmethod
    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = '1m'
    ) -> "DataFrame":
        """Tick adatok átalakítása OHLCV gyertyákká a megadott időkeretben.

        Args:
            symbol: A kereskedési szimbólum (pl. 'EURUSD')
            start: A kezdő időpont
            end: A záró időpont
            timeframe: Az időkeret (alapértelmezett: '1m' - 1 perc)

        Returns:
            DataFrame: OHLCV gyertyákat tartalmazó DataFrame

        Raises:
            ResamplerError: Ha hiba történik az átalakítás során
        """
        pass
