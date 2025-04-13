"""
Adattároló template a Neural-AI-Next projekthez.

Ez a fájl egy adattároló komponens sablont tartalmaz,
amely különböző adattípusok tárolását és kezelését végzi.
"""

import datetime as dt
import os
import pickle
from typing import Any, BinaryIO, Dict, List, Optional, Union

import pandas as pd

from neural_ai.core.logger import LoggerInterface
from neural_ai.core.storage.exceptions import (
    DataNotFoundError,
    InvalidFormatError,
    StorageError,
    StorageWriteError,
)
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class StorageImplementation(StorageInterface):
    """Storage template implementáció."""

    def __init__(self, config: Dict[str, Any], logger: LoggerInterface = None):
        """
        Storage template inicializálása.

        Args:
            config: Konfigurációs beállítások
            logger: Logger példány
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)

        # Konfigurációs értékek beolvasása
        self.base_path = config.get("base_path", "data")
        self.format = config.get("format", "csv")

        # Alapkönyvtár létrehozása
        os.makedirs(self.base_path, exist_ok=True)

    def _get_path(self, symbol: str, timeframe: str, data_type: str = "raw") -> str:
        """
        Fájl útvonal generálása.

        Args:
            symbol: Kereskedési szimbólum
            timeframe: Időkeret
            data_type: Adattípus (raw, processed)

        Returns:
            str: A fájl útvonala
        """
        if data_type == "raw":
            directory = os.path.join(self.base_path, "raw", symbol, timeframe)
        else:
            directory = os.path.join(self.base_path, "processed", data_type, symbol, timeframe)

        os.makedirs(directory, exist_ok=True)

        if self.format == "csv":
            filename = "data.csv"
        elif self.format == "hdf":
            filename = "data.h5"
        elif self.format == "pickle":
            filename = "data.pkl"
        else:
            raise InvalidFormatError(f"Nem támogatott formátum: {self.format}")

        return os.path.join(directory, filename)

    def save_raw_data(
        self, data: Any, symbol: str, timeframe: str, overwrite: bool = False
    ) -> bool:
        """
        Nyers adatok mentése.

        Args:
            data: Mentendő adatok DataFrame formájában
            symbol: Szimbólum (pl. 'EURUSD')
            timeframe: Időkeret (pl. 'M1', 'H1', 'D1')
            overwrite: Ha True, felülírja a meglévő adatokat

        Returns:
            bool: Sikeres mentés esetén True

        Raises:
            StorageError: Tárolási hiba esetén
        """
        try:
            path = self._get_path(symbol, timeframe, "raw")

            if self.format == "csv":
                data.to_csv(path)
            elif self.format == "hdf":
                data.to_hdf(path, key="data", mode="w")
            elif self.format == "pickle":
                with open(path, "wb") as f:
                    pickle.dump(data, f)

            self.logger.info(f"Nyers adatok mentve: {symbol} {timeframe}")
            return True

        except Exception as e:
            self.logger.error(f"Hiba a nyers adatok mentése közben: {str(e)}")
            raise StorageError(f"Adatmentési hiba: {str(e)}")

    def load_raw_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[Union[str, dt.datetime]] = None,
        end_date: Optional[Union[str, dt.datetime]] = None,
        columns: Optional[List[str]] = None,
    ) -> Any:
        """
        Nyers adatok betöltése.

        Args:
            symbol: Szimbólum (pl. 'EURUSD')
            timeframe: Időkeret (pl. 'M1', 'H1', 'D1')
            start_date: Kezdő dátum szűréshez
            end_date: Záró dátum szűréshez
            columns: Betöltendő oszlopok

        Returns:
            pd.DataFrame: A betöltött adatok

        Raises:
            DataNotFoundError: Ha az adatok nem találhatók
            StorageError: Egyéb tárolási hiba esetén
        """
        try:
            path = self._get_path(symbol, timeframe, "raw")

            if not os.path.exists(path):
                raise DataNotFoundError(f"Nincs adat ehhez: {symbol} {timeframe}")

            # Adatok betöltése formátum alapján
            if self.format == "csv":
                data = pd.read_csv(path, index_col=0, parse_dates=True)
            elif self.format == "hdf":
                data = pd.read_hdf(path, key="data")
            elif self.format == "pickle":
                with open(path, "rb") as f:
                    data = pickle.load(f)

            # Dátumszűrés
            if start_date is not None or end_date is not None:
                data = self._filter_by_date(data, start_date, end_date)

            # Oszlopszűrés
            if columns is not None:
                data = data[columns]

            self.logger.info(f"Nyers adatok betöltve: {symbol} {timeframe}")
            return data

        except DataNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Hiba a nyers adatok betöltése közben: {str(e)}")
            raise StorageError(f"Adatbetöltési hiba: {str(e)}")

    def _filter_by_date(
        self,
        data: pd.DataFrame,
        start_date: Optional[Union[str, dt.datetime]],
        end_date: Optional[Union[str, dt.datetime]],
    ) -> pd.DataFrame:
        """
        DataFrame szűrése dátum alapján.

        Args:
            data: Szűrendő DataFrame
            start_date: Kezdő dátum
            end_date: Záró dátum

        Returns:
            pd.DataFrame: Szűrt DataFrame
        """
        filtered_data = data

        # Kezdő dátum szűrés
        if start_date is not None:
            if isinstance(start_date, str):
                start_date = pd.to_datetime(start_date)
            filtered_data = filtered_data[filtered_data.index >= start_date]

        # Záró dátum szűrés
        if end_date is not None:
            if isinstance(end_date, str):
                end_date = pd.to_datetime(end_date)
            filtered_data = filtered_data[filtered_data.index <= end_date]

        return filtered_data

    # Has_data implementáció refaktorálva a komplexitás csökkentése érdekében
    def has_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[Union[str, dt.datetime]] = None,
        end_date: Optional[Union[str, dt.datetime]] = None,
    ) -> bool:
        """
        Ellenőrzi, hogy létezik-e adat a megadott szimbólumhoz és időkerethez.

        Args:
            symbol: Szimbólum (pl. 'EURUSD')
            timeframe: Időkeret (pl. 'M1', 'H1', 'D1')
            start_date: Kezdő dátum (opcionális)
            end_date: Záró dátum (opcionális)

        Returns:
            bool: True, ha létezik adat, False egyébként
        """
        # Ellenőrizzük, hogy létezik-e a fájl
        path = self._get_path(symbol, timeframe, "raw")
        if not os.path.exists(path):
            return False

        # Ha nincs dátumszűrés, akkor csak a fájl létezését ellenőrizzük
        if start_date is None and end_date is None:
            return True

        # Ha van dátumszűrés, ellenőrizzük, hogy a kért dátumtartomány elérhető-e
        return self._check_date_range_exists(path, start_date, end_date)

    # A has_data metódus egy része külön metódusba kiemelve a komplexitás csökkentésére
    def _check_date_range_exists(
        self,
        path: str,
        start_date: Optional[Union[str, dt.datetime]],
        end_date: Optional[Union[str, dt.datetime]],
    ) -> bool:
        """
        Ellenőrzi, hogy a megadott dátumtartomány elérhető-e az adott fájlban.

        Args:
            path: Fájl útvonala
            start_date: Kezdő dátum (opcionális)
            end_date: Záró dátum (opcionális)

        Returns:
            bool: True, ha a dátumtartomány elérhető, False egyébként
        """
        try:
            # Dátumtartomány lekérése formátumtól függően
            if self.format == "csv":
                # Csak az index oszlopot töltjük be (első oszlop)
                df = pd.read_csv(path, index_col=0, parse_dates=True, usecols=[0])
                min_date = df.index.min()
                max_date = df.index.max()
            elif self.format == "hdf":
                with pd.HDFStore(path, mode="r") as store:
                    # Csak az index első és utolsó értékét olvassuk ki
                    min_date = store.select("data", start=0, stop=1).index.min()
                    max_date = store.select(
                        "data",
                        start=store.get_storer("data").nrows - 1,
                        stop=store.get_storer("data").nrows,
                    ).index.max()
            else:  # pickle
                # Nincs optimalizált megoldás, betöltjük az egész adathalmazt
                with open(path, "rb") as f:
                    df = pickle.load(f)
                min_date = df.index.min()
                max_date = df.index.max()

            # Dátumok konvertálása azonos formátumra
            if isinstance(start_date, str):
                start_date = pd.Timestamp(start_date)
            if isinstance(end_date, str):
                end_date = pd.Timestamp(end_date)

            # Ellenőrzés, hogy átfed-e a kért dátumtartomány az adatok dátumtartományával
            if start_date is not None and max_date < start_date:
                return False
            if end_date is not None and min_date > end_date:
                return False

            return True

        except Exception as e:
            self.logger.warning(f"Hiba a dátumtartomány ellenőrzésekor: {str(e)}")
            # Hiba esetén a biztonság kedvéért False-t adunk vissza
            return False
