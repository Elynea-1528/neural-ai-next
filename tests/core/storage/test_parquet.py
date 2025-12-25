"""Tesztek a ParquetStorageService backend selector implementációjához.

Ez a modul tartalmazza a ParquetStorageService tesztjeit, amelyek ellenőrzik
a hardver-gyorsítás detektálást és a backend selector működését.
"""

import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService


class TestParquetStorageService:
    """ParquetStorageService tesztosztály."""

    @pytest.fixture
    def temp_dir(self):
        """Ideiglenes könyvtár létrehozása a tesztekhez."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def service_polars(self, temp_dir):
        """PolarsBackend-et használó szolgáltatás létrehozása."""
        with patch("neural_ai.core.storage.parquet.ParquetStorageService.BASE_PATH", temp_dir):
            with patch("neural_ai.core.utils.hardware.has_avx2", return_value=True):
                service = ParquetStorageService()
                assert service.engine == "polars"
                assert service.backend.name == "polars"
                yield service

    @pytest.fixture
    def service_pandas(self, temp_dir):
        """PandasBackend-et használó szolgáltatás létrehozása."""
        with patch("neural_ai.core.storage.parquet.ParquetStorageService.BASE_PATH", temp_dir):
            with patch("neural_ai.core.utils.hardware.has_avx2", return_value=False):
                service = ParquetStorageService()
                assert service.engine == "fastparquet"
                assert service.backend.name == "pandas"
                yield service

    @pytest.mark.parametrize(
        "has_avx2_value,expected_backend", [(True, "polars"), (False, "pandas")]
    )
    def test_backend_selection_based_on_avx2(self, temp_dir, has_avx2_value, expected_backend):
        """Teszteli a backend kiválasztást az AVX2 támogatás alapján."""
        with patch("neural_ai.core.storage.parquet.ParquetStorageService.BASE_PATH", temp_dir):
            with patch("neural_ai.core.utils.hardware.has_avx2", return_value=has_avx2_value):
                service = ParquetStorageService()

                assert service.backend.name == expected_backend
                if expected_backend == "polars":
                    assert service.engine == "polars"
                else:
                    assert service.engine == "fastparquet"

    @pytest.mark.asyncio
    async def test_store_and_read_tick_data_polars(self, service_polars):
        """Teszteli az adattárolást és -olvasást PolarsBackend-el."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)

        # Tesztadatok létrehozása
        if service_polars.engine == "polars":
            import polars as pl

            data = pl.DataFrame(
                {
                    "timestamp": [
                        datetime(2023, 12, 23, 10, 0, 0),
                        datetime(2023, 12, 23, 10, 1, 0),
                    ],
                    "bid": [1.1000, 1.1001],
                    "ask": [1.1002, 1.1003],
                    "volume": [1000, 1200],
                }
            )
        else:
            import pandas as pd

            data = pd.DataFrame(
                {
                    "timestamp": [
                        datetime(2023, 12, 23, 10, 0, 0),
                        datetime(2023, 12, 23, 10, 1, 0),
                    ],
                    "bid": [1.1000, 1.1001],
                    "ask": [1.1002, 1.1003],
                    "volume": [1000, 1200],
                }
            )

        # Adatok tárolása
        await service_polars.store_tick_data(symbol, data, date)

        # Ellenőrzés, hogy a fájl létrejött-e
        expected_path = service_polars._get_path(symbol, date)
        assert expected_path.exists(), f"Expected file not found: {expected_path}"

        # Adatok olvasása
        start_date = datetime(2023, 12, 23, 0, 0, 0)
        end_date = datetime(2023, 12, 23, 23, 59, 59)
        read_data = await service_polars.read_tick_data(symbol, start_date, end_date)

        # Ellenőrzés
        assert len(read_data) == 2
        if service_polars.engine == "polars":
            assert "timestamp" in read_data.columns
            assert "bid" in read_data.columns
            assert "ask" in read_data.columns
        else:
            assert "timestamp" in read_data.columns
            assert "bid" in read_data.columns
            assert "ask" in read_data.columns

    @pytest.mark.asyncio
    async def test_store_and_read_tick_data_pandas(self, temp_dir):
        """Teszteli az adattárolást és -olvasást PandasBackend-el."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)
        
        # Mock has_avx2 to return False to force Pandas backend
        with patch("neural_ai.core.storage.parquet.has_avx2", return_value=False):
            with patch("neural_ai.core.storage.parquet.ParquetStorageService.BASE_PATH", temp_dir):
                service = ParquetStorageService()
                assert service.backend.name == "pandas"
                
                # Tesztadatok létrehozása
                import pandas as pd
                
                data = pd.DataFrame(
                    {
                        "timestamp": [
                            datetime(2023, 12, 23, 10, 0, 0),
                            datetime(2023, 12, 23, 10, 1, 0),
                        ],
                        "bid": [1.1000, 1.1001],
                        "ask": [1.1002, 1.1003],
                        "volume": [1000, 1200],
                    }
                )
                
                # Adatok tárolása
                await service.store_tick_data(symbol, data, date)
                
                # Ellenőrzés, hogy a fájl létrejött-e
                expected_path = service._get_path(symbol, date)
                assert expected_path.exists(), f"Expected file not found: {expected_path}"
                
                # Adatok olvasása
                start_date = datetime(2023, 12, 23, 0, 0, 0)
                end_date = datetime(2023, 12, 23, 23, 59, 59)
                read_data = await service.read_tick_data(symbol, start_date, end_date)
                
                # Ellenőrzés
                assert len(read_data) == 2
                assert "timestamp" in read_data.columns
                assert "bid" in read_data.columns
                assert "ask" in read_data.columns

    @pytest.mark.asyncio
    async def test_store_empty_dataframe_raises_error(self, service_polars):
        """Teszteli, hogy üres DataFrame tárolása hibát dob."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)

        if service_polars.engine == "polars":
            import polars as pl

            empty_data = pl.DataFrame()
        else:
            import pandas as pd

            empty_data = pd.DataFrame()

        with pytest.raises(ValueError, match="Cannot store empty DataFrame"):
            await service_polars.store_tick_data(symbol, empty_data, date)

    @pytest.mark.asyncio
    async def test_store_missing_required_columns_raises_error(self, service_polars):
        """Teszteli, hogy hiányzó kötelező oszlopok esetén hiba keletkezik."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)

        if service_polars.engine == "polars":
            import polars as pl

            data = pl.DataFrame(
                {"timestamp": [datetime.now()], "bid": [1.1000]}
            )  # Hiányzik az 'ask'
        else:
            import pandas as pd

            data = pd.DataFrame(
                {"timestamp": [datetime.now()], "bid": [1.1000]}
            )  # Hiányzik az 'ask'

        with pytest.raises(ValueError, match="Missing required columns"):
            await service_polars.store_tick_data(symbol, data, date)

    @pytest.mark.asyncio
    async def test_get_available_dates(self, service_polars):
        """Teszteli az elérhető dátumok lekérdezését."""
        symbol = "TESTEURUSD"

        # Hozzunk létre néhány tesztadatot különböző dátumokra
        dates = [datetime(2023, 12, 23), datetime(2023, 12, 24)]

        if service_polars.engine == "polars":
            import polars as pl
        else:
            import pandas as pd

        for date in dates:
            if service_polars.engine == "polars":
                data = pl.DataFrame(
                    {
                        "timestamp": [date],
                        "bid": [1.1000],
                        "ask": [1.1002],
                        "volume": [1000],
                    }
                )
            else:
                data = pd.DataFrame(
                    {
                        "timestamp": [date],
                        "bid": [1.1000],
                        "ask": [1.1002],
                        "volume": [1000],
                    }
                )

            await service_polars.store_tick_data(symbol, data, date)

        # Elérhető dátumok lekérdezése
        available_dates = await service_polars.get_available_dates(symbol)

        assert len(available_dates) == 2
        assert dates[0] in available_dates
        assert dates[1] in available_dates

    @pytest.mark.asyncio
    async def test_calculate_checksum(self, service_polars):
        """Teszteli a checksum számítást."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)

        if service_polars.engine == "polars":
            import polars as pl

            data = pl.DataFrame(
                {
                    "timestamp": [datetime(2023, 12, 23, 10, 0, 0)],
                    "bid": [1.1000],
                    "ask": [1.1002],
                    "volume": [1000],
                }
            )
        else:
            import pandas as pd

            data = pd.DataFrame(
                {
                    "timestamp": [datetime(2023, 12, 23, 10, 0, 0)],
                    "bid": [1.1000],
                    "ask": [1.1002],
                    "volume": [1000],
                }
            )

        await service_polars.store_tick_data(symbol, data, date)

        # Checksum számítása
        checksum = await service_polars.calculate_checksum(symbol, date)

        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA256 hash hossza

    @pytest.mark.asyncio
    async def test_verify_data_integrity(self, service_polars):
        """Teszteli az adatintegritás ellenőrzést."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)

        if service_polars.engine == "polars":
            import polars as pl

            data = pl.DataFrame(
                {
                    "timestamp": [
                        datetime(2023, 12, 23, 10, 0, 0),
                        datetime(2023, 12, 23, 10, 1, 0),
                    ],
                    "bid": [1.1000, 1.1001],
                    "ask": [1.1002, 1.1003],
                    "volume": [1000, 1200],
                }
            )
        else:
            import pandas as pd

            data = pd.DataFrame(
                {
                    "timestamp": [
                        datetime(2023, 12, 23, 10, 0, 0),
                        datetime(2023, 12, 23, 10, 1, 0),
                    ],
                    "bid": [1.1000, 1.1001],
                    "ask": [1.1002, 1.1003],
                    "volume": [1000, 1200],
                }
            )

        await service_polars.store_tick_data(symbol, data, date)

        # Adatintegritás ellenőrzése
        is_valid = await service_polars.verify_data_integrity(symbol, date)

        assert is_valid is True

    @pytest.mark.asyncio
    async def test_get_storage_stats(self, service_polars):
        """Teszteli a tárolási statisztikák lekérdezését."""
        symbol = "TESTEURUSD"
        date = datetime(2023, 12, 23)

        if service_polars.engine == "polars":
            import polars as pl

            data = pl.DataFrame(
                {
                    "timestamp": [datetime(2023, 12, 23, 10, 0, 0)],
                    "bid": [1.1000],
                    "ask": [1.1002],
                    "volume": [1000],
                }
            )
        else:
            import pandas as pd

            data = pd.DataFrame(
                {
                    "timestamp": [datetime(2023, 12, 23, 10, 0, 0)],
                    "bid": [1.1000],
                    "ask": [1.1002],
                    "volume": [1000],
                }
            )

        await service_polars.store_tick_data(symbol, data, date)

        # Statisztikák lekérdezése
        stats = await service_polars.get_storage_stats(symbol)

        assert "total_files" in stats
        assert "total_size_gb" in stats
        assert "symbols" in stats
        assert stats["total_files"] >= 1
        assert stats["total_size_gb"] >= 0
