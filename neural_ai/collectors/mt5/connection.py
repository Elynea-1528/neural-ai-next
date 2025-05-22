"""MT5 kapcsolatkezelő modul."""

from datetime import datetime
from typing import Dict, List, Optional, Union

import pandas as pd


class MT5Connection:
    """MetaTrader 5 kapcsolatkezelő osztály."""

    def __init__(self, config: Dict):
        """Inicializálás konfiguráció alapján."""
        self.config = config
        self._connected = False

    async def connect(self) -> bool:
        """Kapcsolódás az MT5 platformhoz."""
        # TODO: Implementáljuk a valós kapcsolódási logikát
        self._connected = True
        return True

    async def disconnect(self) -> bool:
        """Kapcsolat bontása."""
        self._connected = False
        return True

    def is_connected(self) -> bool:
        """Kapcsolat állapotának lekérdezése."""
        return self._connected

    async def fetch_data(  # pylint: disable=unused-argument
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        max_candles: Optional[int] = None,
    ) -> pd.DataFrame:
        """Adatok lekérése az MT5 platformról.

        Args:
            symbol: Kereskedési szimbólum (pl. EURUSD)
            timeframe: Időkeret (pl. M1, H1)
            start_date: Kezdő dátum
            end_date: Záró dátum
            max_candles: Maximum gyertyák száma

        Returns:
            DataFrame az OHLCV adatokkal
        """
        # TODO: Implementáljuk a valós adatlekérést
        return pd.DataFrame()

    async def get_symbols(self) -> List[str]:
        """Elérhető szimbólumok listájának lekérése."""
        # TODO: Implementáljuk a valós szimbólumlistázást
        return ["EURUSD", "GBPUSD", "USDJPY"]
