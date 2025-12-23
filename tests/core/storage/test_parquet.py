"""ParquetStorageService tesztek.

Ez a modul tartalmazza a ParquetStorageService osztály tesztjeit.
"""

import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl
import pytest

from neural_ai.core.storage.parquet import ParquetStorageService


class TestParquetStorageService:
    """ParquetStorageService tesztosztály."""

    @pytest.fixture
    def temp_dir(self):
        """Ideiglenes könyvtár létrehozása a tesztekhez."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        # Takarítás
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def storage_service(self, temp_dir, monkeypatch):
        """ParquetStorageService példány létrehozása ideiglenes könyvtárral."""
        service = ParquetStorageService()
        # Ideiglenes útvonal beállítása
        monkeypatch.setattr(service, "BASE_PATH", temp_dir)
        return service

    @pytest.fixture
    def sample_tick_data(self):
        """Minta Tick adatok létrehozása."""
        return pl.DataFrame(
            {
                "timestamp": [
                    datetime(2023, 12, 23, 10, 0, 0),
                    datetime(2023, 12, 23, 10, 0, 1),
                    datetime(2023, 12, 23, 10, 0, 2),
                ],
                "bid": [1.1000, 1.1001, 1.1002],
                "ask": [1.1002, 1.1003, 1.1004],
                "volume": [1000, 1200, 1100],
                "source": ["jforex", "jforex", "jforex"],
            }
        )

    @pytest.mark.asyncio
    async def test_store_and_read_tick_data(self, storage_service, sample_tick_data):
        """Tick adatok tárolásának és olvasásának tesztelése."""
        symbol = "EURUSD"
        date = datetime(2023, 12, 23)

        # Adatok tárolása
        await storage_service.store_tick_data(symbol, sample_tick_data, date)

        # Adatok olvasása
        result = await storage_service.read_tick_data(
            symbol, datetime(2023, 12, 23, 9, 0, 0), datetime(2023, 12, 23, 11, 0, 0)
        )

        # Ellenőrzések
        assert len(result) == 3
        assert result.columns == sample_tick_data.columns
        assert result["bid"].to_list() == [1.1000, 1.1001, 1.1002]

    @pytest.mark.asyncio
    async def test_store_empty_dataframe_raises_error(self, storage_service):
        """Üres DataFrame tárolásakor hiba keletkezik."""
        empty_df = pl.DataFrame({"timestamp": [], "bid": [], "ask": []})

        with pytest.raises(ValueError, match="Cannot store empty DataFrame"):
            await storage_service.store_tick_data("EURUSD", empty_df, datetime.now())

    @pytest.mark.asyncio
    async def test_store_missing_required_columns_raises_error(self, storage_service):
        """Hiányzó kötelező oszlopok esetén hiba keletkezik."""
        incomplete_df = pl.DataFrame(
            {
                "timestamp": [datetime.now()],
                "bid": [1.1000],
                # 'ask' oszlop hiányzik
            }
        )

        with pytest.raises(ValueError, match="Missing required columns"):
            await storage_service.store_tick_data("EURUSD", incomplete_df, datetime.now())

    @pytest.mark.asyncio
    async def test_read_nonexistent_data_returns_empty_dataframe(self, storage_service):
        """Nem létező adatok olvasásakor üres DataFrame tér vissza."""
        result = await storage_service.read_tick_data(
            "EURUSD", datetime(2023, 1, 1), datetime(2023, 1, 2)
        )

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_available_dates(self, storage_service, sample_tick_data):
        """Elérhető dátumok lekérdezésének tesztelése."""
        symbol = "EURUSD"

        # Több nap adatainak tárolása
        dates = [datetime(2023, 12, 23), datetime(2023, 12, 24), datetime(2023, 12, 25)]

        for date in dates:
            await storage_service.store_tick_data(symbol, sample_tick_data, date)

        # Elérhető dátumok lekérdezése
        available_dates = await storage_service.get_available_dates(symbol)

        # Ellenőrzések
        assert len(available_dates) == 3
        assert available_dates == sorted(dates)

    @pytest.mark.asyncio
    async def test_get_available_dates_nonexistent_symbol(self, storage_service):
        """Nem létező szimbólum dátumainak lekérdezése."""
        dates = await storage_service.get_available_dates("NONEXISTENT")

        assert len(dates) == 0

    @pytest.mark.asyncio
    async def test_calculate_checksum(self, storage_service, sample_tick_data):
        """Checksum számításának tesztelése."""
        symbol = "EURUSD"
        date = datetime(2023, 12, 23)

        # Adatok tárolása
        await storage_service.store_tick_data(symbol, sample_tick_data, date)

        # Checksum számítása
        checksum = await storage_service.calculate_checksum(symbol, date)

        # Ellenőrzések
        assert len(checksum) == 64  # SHA256 hash hossza
        assert checksum != ""

    @pytest.mark.asyncio
    async def test_calculate_checksum_nonexistent_file(self, storage_service):
        """Nem létező fájl checksum számítása."""
        checksum = await storage_service.calculate_checksum("EURUSD", datetime(2023, 1, 1))

        assert checksum == ""

    @pytest.mark.asyncio
    async def test_verify_data_integrity_success(self, storage_service, sample_tick_data):
        """Adatintegritás ellenőrzése sikeres esetben."""
        symbol = "EURUSD"
        date = datetime(2023, 12, 23)

        # Adatok tárolása
        await storage_service.store_tick_data(symbol, sample_tick_data, date)

        # Integritás ellenőrzése
        is_valid = await storage_service.verify_data_integrity(symbol, date)

        assert is_valid is True

    @pytest.mark.asyncio
    async def test_verify_data_integrity_nonexistent_file(self, storage_service):
        """Adatintegritás ellenőrzése nem létező fájl esetén."""
        is_valid = await storage_service.verify_data_integrity("EURUSD", datetime(2023, 1, 1))

        assert is_valid is False

    @pytest.mark.asyncio
    async def test_get_storage_stats(self, storage_service, sample_tick_data):
        """Tárolási statisztikák lekérdezésének tesztelése."""
        symbol = "EURUSD"

        # Több nap adatainak tárolása
        for i in range(3):
            date = datetime(2023, 12, 23 + i)
            await storage_service.store_tick_data(symbol, sample_tick_data, date)

        # Statisztikák lekérdezése
        stats = await storage_service.get_storage_stats()

        # Ellenőrzések
        assert stats["total_files"] == 3
        assert stats["total_size_gb"] > 0
        assert symbol.upper() in stats["symbols"]
        assert stats["symbols"][symbol.upper()]["files"] == 3

    @pytest.mark.asyncio
    async def test_get_storage_stats_specific_symbol(self, storage_service, sample_tick_data):
        """Tárolási statisztikák lekérdezése specifikus szimbólumra."""
        # Két szimbólum adatainak tárolása
        await storage_service.store_tick_data("EURUSD", sample_tick_data, datetime(2023, 12, 23))
        await storage_service.store_tick_data("GBPUSD", sample_tick_data, datetime(2023, 12, 23))

        # Statisztikák lekérdezése csak EURUSD-ra
        stats = await storage_service.get_storage_stats("EURUSD")

        # Ellenőrzések
        assert stats["total_files"] == 1
        assert "EURUSD" in stats["symbols"]
        assert "GBPUSD" not in stats["symbols"]

    @pytest.mark.asyncio
    async def test_read_tick_data_date_filtering(self, storage_service, sample_tick_data):
        """Tick adatok dátum szerinti szűrésének tesztelése."""
        symbol = "EURUSD"
        date = datetime(2023, 12, 23)

        # Adatok tárolása
        await storage_service.store_tick_data(symbol, sample_tick_data, date)

        # Szűkebb dátumtartomány lekérdezése
        result = await storage_service.read_tick_data(
            symbol, datetime(2023, 12, 23, 10, 0, 1), datetime(2023, 12, 23, 10, 0, 2)
        )

        # Ellenőrzések
        assert len(result) == 2
        assert result["timestamp"].to_list() == [
            datetime(2023, 12, 23, 10, 0, 1),
            datetime(2023, 12, 23, 10, 0, 2),
        ]

    @pytest.mark.asyncio
    async def test_symbol_case_insensitivity(self, storage_service, sample_tick_data):
        """Szimbólumok kis- és nagybetű érzékenységének tesztelése."""
        # Adatok tárolása kisbetűvel
        await storage_service.store_tick_data("eurusd", sample_tick_data, datetime.now())

        # Adatok olvasása nagybetűvel
        result = await storage_service.read_tick_data(
            "EURUSD", datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1)
        )

        # Ellenőrzések
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_multiple_symbols_storage(self, storage_service, sample_tick_data):
        """Több szimbólum egyidejű tárolásának tesztelése."""
        symbols = ["EURUSD", "GBPUSD", "USDJPY"]

        # Adatok tárolása minden szimbólumhoz
        for symbol in symbols:
            await storage_service.store_tick_data(symbol, sample_tick_data, datetime(2023, 12, 23))

        # Ellenőrzés, hogy minden szimbólumhoz tartozik-e adat
        stats = await storage_service.get_storage_stats()

        assert stats["total_files"] == 3
        for symbol in symbols:
            assert symbol.upper() in stats["symbols"]
            assert stats["symbols"][symbol.upper()]["files"] == 1
