"""Adatgyűjtő template a Neural-AI-Next projekthez.

Ez a fájl egy adatgyűjtő komponens sablont tartalmaz, amely különböző
forrásokból (például MT5, API-k, fájlok) származó adatok beszerzésére szolgál.
"""

import datetime as dt
from typing import Any

import pandas as pd
from neural_ai.collectors.interfaces import CollectorInterface

from neural_ai.core.logger import LoggerFactory
from neural_ai.core.storage import StorageFactory


class DataCollector(CollectorInterface):
    """Adatgyűjtő komponens.

    Ez a komponens adatokat gyűjt különböző forrásokból és egységes formátumra alakítja.

    Attributes:
        config: Gyűjtő konfiguráció
        source_type: Az adatforrás típusa
        logger: Logger példány
        storage: Tároló példány az adatok mentéséhez
    """

    def __init__(self, config: dict[str, Any], logger=None, storage=None):
        """Inicializálja az adatgyűjtőt.

        Args:
            config: Adatgyűjtő konfigurációja
            logger: Logger példány vagy None (ekkor alapértelmezett logger jön létre)
            storage: Storage példány vagy None (ekkor alapértelmezett storage jön létre)
        """
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)

        # Konfigurációs paraméterek beolvasása
        self.source_type = config.get("source_type", "unknown")
        self.cache_data = config.get("cache_data", True)
        self.timeout = config.get("timeout", 30)

        # Storage inicializálása
        self.storage = storage or StorageFactory.get_storage(config.get("storage", {}))

        # Forrás specifikus inicializáció
        self._init_source()

        self.logger.info(f"{self.__class__.__name__} initialized for source {self.source_type}")

    def _init_source(self):
        """Adatforrás specifikus inicializáció.

        Raises:
            ConnectionError: Ha a kapcsolat nem hozható létre
        """
        try:
            # Forrás specifikus inicializáció (például API kapcsolat, fájl megnyitás)
            # Az implementációt a leszármazott osztályok felülírhatják
            pass
        except Exception as e:
            self.logger.error(f"Failed to initialize source {self.source_type}: {str(e)}")
            raise ConnectionError(f"Source initialization failed: {str(e)}") from e

    def collect(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None = None,
        end_date: str | dt.datetime | None = None,
    ) -> pd.DataFrame:
        """Adatok gyűjtése a megadott szimbólumhoz és időkerethez.

        Args:
            symbol: Kereskedési szimbólum (pl. "EURUSD")
            timeframe: Időkeret (pl. "M1", "H1", "D1")
            start_date: Kezdő dátum
            end_date: Záró dátum

        Returns:
            Gyűjtött adatok pandas DataFrame formában

        Raises:
            CollectorError: Adatgyűjtési hiba esetén
        """
        self.logger.info(
            f"Collecting data for {symbol} {timeframe} from {start_date} to {end_date}"
        )

        try:
            # Ellenőrizzük, hogy van-e már mentett adat
            if self.cache_data and self.storage.has_data(symbol, timeframe, start_date, end_date):
                self.logger.debug(f"Loading cached data for {symbol} {timeframe}")
                return self.storage.load_raw_data(symbol, timeframe, start_date, end_date)

            # Adatok lekérése a forrásból
            data = self._fetch_data(symbol, timeframe, start_date, end_date)

            # Adatok formázása
            data = self._format_data(data)

            # Adatok mentése (ha be van kapcsolva a gyorsítótárazás)
            if self.cache_data:
                self.storage.save_raw_data(data, symbol, timeframe)

            self.logger.info(f"Successfully collected {len(data)} rows for {symbol} {timeframe}")
            return data

        except Exception as e:
            self.logger.error(f"Error collecting data for {symbol} {timeframe}: {str(e)}")
            raise CollectorError(f"Data collection failed: {str(e)}") from e

    def _fetch_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: str | dt.datetime | None,
        end_date: str | dt.datetime | None,
    ) -> pd.DataFrame:
        """Adatok lekérése a forrásból.

        Args:
            symbol: Kereskedési szimbólum
            timeframe: Időkeret
            start_date: Kezdő dátum
            end_date: Záró dátum

        Returns:
            Lekért nyers adatok

        Raises:
            NotImplementedError: Az implementáció a leszármazott osztályokban kell
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def _format_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Adatok formázása egységes formátumra.

        Args:
            data: Nyers adatok

        Returns:
            Formázott adatok
        """
        # Az alapértelmezett implementáció feltételezi, hogy az adatok már
        # a megfelelő formátumban vannak. A leszármazott osztályok felülírhatják.

        # Ellenőrizzük a kötelező oszlopokat
        required_columns = ["open", "high", "low", "close", "volume", "time"]
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            self.logger.warning(f"Missing required columns: {missing_columns}")
            # Hiányzó oszlopok létrehozása (alapértelmezett értékekkel)
            for col in missing_columns:
                data[col] = None

        # Időbélyeg beállítása index-ként
        if "time" in data.columns and not data.index.equals(data["time"]):
            data.set_index("time", inplace=True)

        return data

    def get_available_symbols(self) -> list[str]:
        """Elérhető szimbólumok lekérése.

        Returns:
            Az adatforrásban elérhető szimbólumok listája
        """
        # Implementáció...
        return []

    def get_available_timeframes(self) -> list[str]:
        """Elérhető időkeretek lekérése.

        Returns:
            Az adatforrásban elérhető időkeretek listája
        """
        # Implementáció...
        return []

    def close(self):
        """Adatforrás kapcsolat lezárása és erőforrások felszabadítása."""
        # Implementáció...
        self.logger.info(f"Closed collector for source {self.source_type}")


class CollectorError(Exception):
    """Az adatgyűjtő specifikus kivétele."""

    pass


class CollectorFactory:
    """Factory osztály az adatgyűjtők létrehozásához."""

    @staticmethod
    def get_collector(
        source_type: str, config: dict[str, Any], logger=None, storage=None
    ) -> CollectorInterface:
        """Adatgyűjtő példány létrehozása.

        Args:
            source_type: Adatforrás típusa (pl. "mt5", "api", "csv")
            config: Adatgyűjtő konfiguráció
            logger: Opcionális logger példány
            storage: Opcionális storage példány

        Returns:
            CollectorInterface: Adatgyűjtő példány

        Raises:
            ValueError: Ismeretlen adatforrás típus esetén
        """
        # Ellenőrizzük, hogy a konfiguráció tartalmazza-e a forrás típust
        source_config = config.copy()
        source_config["source_type"] = source_type

        # A megfelelő implementáció kiválasztása
        if source_type == "mt5":
            from neural_ai.collectors.mt5_collector import MT5Collector

            return MT5Collector(source_config, logger, storage)
        elif source_type == "csv":
            from neural_ai.collectors.csv_collector import CSVCollector

            return CSVCollector(source_config, logger, storage)
        elif source_type == "api":
            from neural_ai.collectors.api_collector import APICollector

            return APICollector(source_config, logger, storage)
        else:
            raise ValueError(f"Unknown source type: {source_type}")
