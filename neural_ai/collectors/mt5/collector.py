"""MT5 Collector komponens fő osztálya."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from neural_ai.core.config import ConfigManagerFactory
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory
from neural_ai.core.storage.implementations.storage_factory import StorageFactory

from .connection import MT5Connection
from .validator import DataValidator

logger = LoggerFactory.get_logger(__name__)


class MT5CollectorError(Exception):
    """Alap kivétel az MT5 Collector komponenshez."""


class MT5ConnectionError(MT5CollectorError):
    """Kapcsolódási hibák."""


class DataFetchError(MT5CollectorError):
    """Adatok lekérésével kapcsolatos hibák."""


class ValidationError(MT5CollectorError):
    """Adat validációs hibák."""


class ConfigurationError(MT5CollectorError):
    """Konfigurációs hibák."""


class MT5Collector:
    """MetaTrader 5 adatgyűjtő komponens."""

    def __init__(self, config_path: str):
        """Inicializálás konfigurációs fájl alapján."""
        try:
            config_manager = ConfigManagerFactory.get_manager(config_path)
            self.config = config_manager.get_section("mt5")
            self.connection = MT5Connection(self.config["connection"])
            self.validator = DataValidator()
            self.storage = StorageFactory.get_storage()
        except Exception as e:
            raise ConfigurationError(f"Konfigurációs hiba: {e}") from e

    async def connect(self) -> bool:
        """Kapcsolódás a MetaTrader 5 platformhoz."""
        try:
            connected = await self.connection.connect()
            if not connected:
                logger.error("Nem sikerült kapcsolódni az MT5 platformhoz")
            return connected
        except Exception as e:
            raise MT5ConnectionError(f"Kapcsolódási hiba: {e}") from e

    async def disconnect(self) -> bool:
        """Kapcsolat bontása a MetaTrader 5 platformmal."""
        try:
            return await self.connection.disconnect()
        except Exception as e:
            raise MT5ConnectionError(f"Kapcsolatbontási hiba: {e}") from e

    def is_connected(self) -> bool:
        """Kapcsolat állapotának ellenőrzése."""
        return self.connection.is_connected()

    async def download_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[Union[str, datetime]] = None,
        end_date: Optional[Union[str, datetime]] = None,
        max_candles: Optional[int] = None,
    ) -> pd.DataFrame:
        """Adatok letöltése a megadott szimbólumhoz és időkerethez."""
        try:
            if not self.is_connected():
                await self.connect()

            # Alapértelmezett értékek beállítása
            max_candles = max_candles or self.config["data"]["max_candles"]

            # Adatok letöltése
            raw_data = await self.connection.fetch_data(
                symbol=symbol,
                timeframe=timeframe,
                start_date=start_date,
                end_date=end_date,
                max_candles=max_candles,
            )

            # Adatok validálása
            validated_data = self.validator.validate(raw_data)

            # Adatok tárolása
            self.storage.save_dataframe(path=f"mt5/{symbol}/{timeframe}", df=validated_data)

            return validated_data

        except Exception as e:
            raise DataFetchError(f"Adatlekérési hiba: {e}") from e

    async def get_available_symbols(self) -> List[str]:
        """Elérhető szimbólumok listájának lekérése."""
        try:
            if not self.is_connected():
                await self.connect()
            return await self.connection.get_symbols()
        except Exception as e:
            raise DataFetchError(f"Szimbólumlista lekérési hiba: {e}") from e

    def get_available_timeframes(self) -> Dict[str, int]:
        """Elérhető időkeretek listájának lekérése."""
        return self.config["timeframes"]

    def check_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Adatok minőségének ellenőrzése."""
        return self.validator.check_quality(data)
