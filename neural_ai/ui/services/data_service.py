"""Data Service implementáció.

Ez a modul implementálja az adatkezelési szolgáltatást, amely
az adatok betöltését, szűrését és kezelését végzi Big Data támogatással.
"""

import asyncio
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import pandas as pd
import polars as pl

from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface

if TYPE_CHECKING:
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


class DataService(DataServiceInterface):
    """Data Service - Adatkezelésért felelős.

    Ez az osztály implementálja az adatok lekérdezését és kezelését
    végző metódusokat, Big Data támogatással és chunkolással.
    """

    def __init__(self, bridge: "CoreBridgeInterface") -> None:
        """A Data Service inicializálása.

        Args:
            bridge: A backend bridge példány, amelyen keresztül elérjük a
                backend komponenseket (Bi5Downloader, ParquetStorage)
        """
        self._bridge = bridge
        self._data_sources: dict[str, dict[str, str]] = {
            "tick_data": {
                "name": "Tick Adatok",
                "description": "Valós idejű tick adatok",
                "format": "parquet",
            },
            "ohlc_data": {
                "name": "OHLC Adatok",
                "description": "Nyitó, magas, alacsony, záró adatok",
                "format": "parquet",
            },
            "market_data": {
                "name": "Piaci Adatok",
                "description": "Általános piaci adatok",
                "format": "parquet",
            },
        }

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
        if source not in self._data_sources:
            raise ValueError(f"Ismeretlen adatforrás: {source}")

        # Mock adatok generálása
        # Valós implementációban itt a backend API-t hívnánk meg
        mock_data = self._generate_mock_data(source, filters)

        # Adatok chunkolása
        for i in range(0, len(mock_data), chunk_size):
            chunk = mock_data[i : i + chunk_size]
            yield chunk

    def get_data_sources(self) -> list[dict[str, str]]:
        """Elérhető adatforrások lekérdezése.

        Returns:
            List[Dict[str, str]]: Az adatforrások listája
        """
        sources: list[dict[str, str]] = []
        for source_id, info in self._data_sources.items():
            sources.append(
                {
                    "id": source_id,
                    "name": info["name"],
                    "description": info["description"],
                    "format": info["format"],
                }
            )
        return sources

    def get_data_info(self, source: str) -> dict[str, Any]:
        """Adatforrás információk lekérdezése.

        Args:
            source: Az adatforrás azonosítója

        Returns:
            Dict[str, Any]: Az adatforrás metaadatai
        """
        if source not in self._data_sources:
            raise ValueError(f"Ismeretlen adatforrás: {source}")

        info = self._data_sources[source]
        return {
            "source": source,
            "name": info["name"],
            "description": info["description"],
            "format": info["format"],
            "size": "2.5 GB",  # Mock adat
            "records": 15000000,  # Mock adat
            "last_updated": "2026-01-04T19:00:00Z",
        }

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
        filtered_data = data.copy()

        for key, value in filters.items():
            if isinstance(value, (int, float, str)):
                filtered_data = [item for item in filtered_data if item.get(key) == value]
            elif isinstance(value, dict):
                # Támogatás tartomány szűrésre
                if "min" in value:
                    filtered_data = [
                        item for item in filtered_data if item.get(key, 0) >= value["min"]
                    ]
                if "max" in value:
                    filtered_data = [
                        item
                        for item in filtered_data
                        if item.get(key, float("inf")) <= value["max"]
                    ]

        return filtered_data

    def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool:
        """Adatok exportálása különböző formátumokba.

        Args:
            data: Az exportálandó adatok
            format: A célformátum (parquet, csv, json)
            destination: A cél útvonal

        Returns:
            bool: True, ha sikeres az exportálás
        """
        supported_formats = ["parquet", "csv", "json"]

        if format not in supported_formats:
            raise ValueError(f"Nem támogatott formátum: {format}")

        if not data:
            return False

        # Valós implementációban itt tényleges exportálást végeznénk
        # Most csak szimuláljuk a műveletet
        print(f"Exportálás {len(data)} rekord {format} formátumban ide: {destination}")

        return True

    def _generate_mock_data(
        self, source: str, filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Mock adatok generálása teszteléshez.

        Args:
            source: Az adatforrás azonosítója
            filters: Szűrőfeltételek

        Returns:
            List[Dict[str, Any]]: A generált mock adatok
        """
        import random

        data: list[dict[str, Any]] = []
        base_time = datetime.now()

        for i in range(1000):
            timestamp = base_time - timedelta(minutes=i)

            if source == "tick_data":
                item: dict[str, Any] = {
                    "timestamp": timestamp.isoformat(),
                    "symbol": "EURUSD",
                    "bid": 1.0850 + random.uniform(-0.001, 0.001),
                    "ask": 1.0852 + random.uniform(-0.001, 0.001),
                    "volume": random.randint(1, 100),
                }
            elif source == "ohlc_data":
                item = {
                    "timestamp": timestamp.isoformat(),
                    "symbol": "EURUSD",
                    "open": 1.0850 + random.uniform(-0.002, 0.002),
                    "high": 1.0860 + random.uniform(-0.002, 0.002),
                    "low": 1.0840 + random.uniform(-0.002, 0.002),
                    "close": 1.0855 + random.uniform(-0.002, 0.002),
                    "volume": random.randint(1000, 10000),
                }
            else:
                item = {
                    "timestamp": timestamp.isoformat(),
                    "symbol": "EURUSD",
                    "price": 1.0850 + random.uniform(-0.001, 0.001),
                    "volume": random.randint(1, 1000),
                }

            data.append(item)

        # Szűrők alkalmazása
        if filters:
            data = self.apply_filters(data, filters)

        return data

    async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]:
        """Történelmi adatok letöltése aszinkron módon.

        Ez a metódus a CoreBridge-en keresztül eléri a Bi5Downloader-t,
        és valós adatletöltést végez a Dukascopy .bi5 formátumból.

        Args:
            symbol: A szimbólum (pl. 'EURUSD')
            start: A kezdő dátum
            end: A záró dátum

        Returns:
            dict[str, Any]: A letöltött adatok metaadatai és az adatok
                - symbol: A letöltött szimbólum
                - start_date: Kezdő dátum ISO formátumban
                - end_date: Záró dátum ISO formátumban
                - status: Letöltési állapot ('downloaded', 'failed', 'partial')
                - records: Letöltött rekordok száma
                - size_mb: Letöltött adatok mérete MB-ban
                - format: Az adatformátum ('parquet')
                - path: A tárolási útvonal

        Raises:
            ValueError: Ha a dátumtartomány érvénytelen
            RuntimeError: Ha a letöltés sikertelen
        """
        # Dátumtartomány ellenőrzése
        if start > end:
            raise ValueError("A kezdő dátum nem lehet későbbi, mint a záró dátum")

        if start > datetime.now(UTC):
            raise ValueError("A kezdő dátum nem lehet a jövőben")

        # CoreBridge-en keresztül lekérjük a Bi5Downloader komponenst
        downloader = self._bridge.get_component("bi5_downloader")
        if downloader is None:
            raise RuntimeError("A Bi5Downloader komponens nem érhető el")

        # Típus ellenőrzés (futási időben)
        from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader

        if not isinstance(downloader, IJForexDownloader):
            raise RuntimeError("A komponens nem implementálja az IJForexDownloader interfészt")

        downloader = cast(IJForexDownloader, downloader)

        try:
            # Storage komponens lekérése a mentéshez
            storage = self._bridge.get_component("parquet_storage")
            if storage is None:
                raise RuntimeError("A ParquetStorage komponens nem érhető el a mentéshez")

            # Típus ellenőrzés (futási időben)
            from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

            if not isinstance(storage, StorageInterface):
                raise RuntimeError("A storage komponens nem implementálja a StorageInterface-t")
            storage = cast(StorageInterface, storage)

            # Dátumok iterálása és adatok letöltése
            current_date = start
            total_records = 0
            successful_dates = 0
            failed_dates = 0

            # Külső ciklus: Napok
            while current_date <= end:
                day_ticks = 0
                day_successful_hours = 0
                day_failed_hours = 0

                # Belső ciklus: Órák (0-23)
                for hour in range(24):
                    # Az aktuális óra időpontjának beállítása
                    target_time = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)

                    # Ha a target_time túlmegy a kért végdátum óráján, akkor break
                    if target_time > end:
                        break

                    try:
                        # Tick adatok letöltése az adott órára
                        tick_data = await downloader.download_tick_data(symbol, target_time)

                        if tick_data:
                            total_records += len(tick_data)
                            day_ticks += len(tick_data)
                            day_successful_hours += 1

                            # Tick adatok konvertálása Polars DataFrame-re
                            tick_dicts = [
                                {
                                    "timestamp": tick.timestamp,
                                    "bid": tick.bid,
                                    "ask": tick.ask,
                                    "ask_volume": tick.ask_volume
                                    if tick.ask_volume is not None
                                    else 0.0,
                                    "bid_volume": tick.bid_volume
                                    if tick.bid_volume is not None
                                    else 0.0,
                                    "source": tick.source,
                                }
                                for tick in tick_data
                            ]

                            df = pl.DataFrame(tick_dicts)

                            # Technikai 'volume' oszlop hozzáadása
                            df = df.with_columns(
                                (pl.col("ask_volume") + pl.col("bid_volume")).alias("volume")
                            )

                            # Adatok mentése a storage-ba (óra szintű unique_id-vel)
                            unique_id = f"{hour:02d}"
                            await storage.store_tick_data(
                                symbol=symbol, data=df, date=target_time, unique_id=unique_id
                            )
                        else:
                            day_failed_hours += 1

                    except Exception as e:
                        print(
                            f"Figyelmeztetés: Nem sikerült letölteni az adatokat "
                            f"a(z) {target_time} időpontra: {e}"
                        )
                        day_failed_hours += 1

                # Nap statisztikája
                if day_successful_hours > 0:
                    successful_dates += 1
                    msg = f"✅ Nap összesítve ({current_date.date()}): "
                    msg += f"{day_successful_hours} óra, {day_ticks} tick"
                    print(msg)
                else:
                    print(f"⚠️  Nap összesítve ({current_date.date()}): Nincs elérhető adat")
                    failed_dates += 1

                if day_failed_hours > 0:
                    msg = f"❌ Nap összesítve ({current_date.date()}): "
                    msg += f"{day_failed_hours} óra sikertelen"
                    print(msg)

                current_date += timedelta(days=1)

            # Állapot meghatározása
            total_days = (end - start).days + 1
            if failed_dates == 0:
                status = "downloaded"
            elif successful_dates > 0:
                status = "partial"
            else:
                status = "failed"

            # Átlagos méret becslése (kb 300 byte per tick)
            estimated_size_mb = (total_records * 300) / (1024 * 1024)

            return {
                "symbol": symbol,
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "status": status,
                "records": total_records,
                "size_mb": round(estimated_size_mb, 2),
                "format": "parquet",
                "path": f"/data/tick/{symbol}/{start.year}/{start.month:02d}/",
                "successful_dates": successful_dates,
                "failed_dates": failed_dates,
                "total_days": total_days,
            }

        except Exception as e:
            raise RuntimeError(f"Adatletöltés sikertelen: {str(e)}") from e

    def list_available_data(self, symbol: str | None = None) -> pd.DataFrame:
        """Elérhető adatok listázása DataFrame formátumban.

        Ez a metódus a CoreBridge-en keresztül eléri a ParquetStorage-t,
        és valós adatokról állít össze listát.

        Args:
            symbol: Opcionális szimbólum szűréshez

        Returns:
            pd.DataFrame: Az elérhető adatok DataFrame-je, amely tartalmazza:
                - source_id: Az adatforrás azonosítója
                - name: Az adatforrás neve
                - description: Leírás
                - format: Az adatformátum
                - size_gb: Méret GB-ban
                - records: Rekordok száma
                - last_updated: Utolsó frissítés időpontja
                - available_dates: Elérhető dátumok száma
        """
        # CoreBridge-en keresztül lekérjük a Storage komponenst
        storage = self._bridge.get_component("parquet_storage")
        if storage is None:
            raise RuntimeError("A ParquetStorage komponens nem érhető el")

        # Típus ellenőrzés
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

        if not isinstance(storage, StorageInterface):
            raise RuntimeError("A komponens nem implementálja a StorageInterface-t")

        storage = cast(StorageInterface, storage)

        try:
            data_records: list[dict[str, Any]] = []

            # Szimbólumok meghatározása
            symbols = [symbol] if symbol else ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "XAUUSD"]

            for sym in symbols:
                # Storage statisztikák lekérdezése
                stats = asyncio.run(self._get_storage_stats_async(storage, sym))

                # Típus konverziók a statisztikákhoz
                total_files = int(stats.get("total_files", 0)) if stats.get("total_files", 0) else 0
                size_gb = float(stats.get("size_gb", 0.0)) if stats.get("size_gb", 0.0) else 0.0
                available_dates = (
                    int(stats.get("available_dates", 0)) if stats.get("available_dates", 0) else 0
                )

                if total_files > 0:
                    for source_id, info in self._data_sources.items():
                        data_records.append(
                            {
                                "source_id": source_id,
                                "symbol": sym,
                                "name": info["name"],
                                "description": info["description"],
                                "format": info["format"],
                                "size_gb": round(size_gb, 2),
                                "records": total_files * 10000,  # Becslés
                                "last_updated": datetime.now().isoformat(),
                                "available_dates": available_dates,
                                "total_files": total_files,
                            }
                        )

            return pd.DataFrame(data_records)

        except Exception as e:
            raise RuntimeError(f"Adatok listázása sikertelen: {str(e)}") from e

    async def _get_storage_stats_async(
        self, storage: "StorageInterface", symbol: str
    ) -> dict[str, Any]:
        """Segédfüggvény a storage statisztikák aszinkron lekérdezéséhez.

        Args:
            storage: A storage interfész példány
            symbol: A szimbólum

        Returns:
            dict[str, Any]: A statisztikák
        """
        try:
            # ParquetStorageService specifikus metódus használata, ha elérhető
            if hasattr(storage, "get_storage_stats"):
                stats_method = storage.get_storage_stats
                # Ha async metódus
                if asyncio.iscoroutinefunction(stats_method):
                    result = await stats_method(symbol)
                    return cast(dict[str, Any], result)
                else:
                    # Ha szinkron metódus, futtatás executorban
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(None, stats_method, symbol)
                    return cast(dict[str, Any], result)
            else:
                # Alap statisztikák, ha a metódus nem elérhető
                return {
                    "total_files": 0,
                    "size_gb": 0.0,
                    "available_dates": 0,
                }
        except Exception:
            # Hibaelnyelés, hogy a UI ne akadjon le
            return {
                "total_files": 0,
                "size_gb": 0.0,
                "available_dates": 0,
            }

    def get_storage_path(self) -> Path:
        """Az adattárolási útvonal lekérdezése.

        Ez a metódus a CoreBridge-en keresztül eléri a ParquetStorage-t,
        és a tényleges tárolási útvonalat adja vissza.

        Returns:
            Path: Az adattárolási útvonal

        Raises:
            RuntimeError: Ha a storage komponens nem érhető el
        """
        # CoreBridge-en keresztül lekérjük a Storage komponenst
        storage = self._bridge.get_component("parquet_storage")
        if storage is None:
            raise RuntimeError("A ParquetStorage komponens nem érhető el")

        # Típus ellenőrzés
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

        if not isinstance(storage, StorageInterface):
            raise RuntimeError("A komponens nem implementálja a StorageInterface-t")

        storage = cast(StorageInterface, storage)

        try:
            # Ha a storage-nak van BASE_PATH attribútuma
            if hasattr(storage, "BASE_PATH"):
                base_path = storage.BASE_PATH
                if isinstance(base_path, (str, Path)):
                    return Path(base_path)

            # Alapértelmezett útvonal, ha nem sikerül lekérni
            return Path("/data/tick")

        except Exception as e:
            raise RuntimeError(f"Tárolási útvonal lekérdezése sikertelen: {str(e)}") from e

    def get_configured_symbols(self) -> list[str]:
        """Konfigurált szimbólumok lekérdezése.

        A metódus eléri a konfigurációt a CoreBridge-en keresztül, és kiolvassa
        a JForex collectorhoz tartozó szimbólumokat. Ha a konfiguráció üres vagy
        hiba történik a lekérdezés során, akkor egy alapértelmezett szimbólumlistát
        ad vissza.

        Returns:
            list[str]: A konfigurált szimbólumok listája. Alapértelmezett esetben
                ["EURUSD"]-t ad vissza, ha a konfigurációból nem sikerül
                lekérdezni a szimbólumokat.

        Examples:
            >>> data_service = DataService(bridge)
            >>> symbols = data_service.get_configured_symbols()
            >>> print(symbols)
            ['EURUSD', 'GBPUSD', 'USDJPY']
        """
        try:
            # Konfiguráció elérése a CoreBridge-en keresztül
            config = self._bridge.core.config
            if config is None:
                return ["EURUSD"]

            # Szimbólumok kiolvasása a konfigurációból
            symbols = config.get("collectors", "jforex", "symbols")

            # Ellenőrzés, hogy a symbols egy lista-e és nem üres
            if isinstance(symbols, list) and symbols:
                return symbols
            else:
                # Fallback, ha üres vagy nem lista
                return ["EURUSD"]

        except Exception:
            # Fallback, ha bármilyen hiba történik
            return ["EURUSD"]
