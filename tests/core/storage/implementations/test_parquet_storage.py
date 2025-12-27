"""ParquetStorageService tesztek.

Ez a modul tartalmazza a ParquetStorageService osztály tesztjeit,
beleértve a backend kiválasztást, adattárolást, adatolvasást és
integritás ellenőrzést.
"""

import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import polars as pl
import pytest

from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService


class TestParquetStorageService:
    """ParquetStorageService osztály tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Ideiglenes könyvtár létrehozása a tesztekhez."""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        shutil.rmtree(tmpdir)

    @pytest.fixture
    def sample_pandas_data(self) -> pd.DataFrame:
        """Minta Pandas DataFrame létrehozása."""
        return pd.DataFrame(
            {
                "timestamp": [
                    datetime(2023, 12, 23, 10, 0, 0),
                    datetime(2023, 12, 23, 10, 1, 0),
                    datetime(2023, 12, 23, 10, 2, 0),
                ],
                "bid": [1.1000, 1.1001, 1.1002],
                "ask": [1.1002, 1.1003, 1.1004],
                "volume": [1000, 1200, 1100],
                "source": ["jforex", "jforex", "jforex"],
            }
        )

    @pytest.fixture
    def sample_polars_data(self) -> pl.DataFrame:
        """Minta Polars DataFrame létrehozása."""
        return pl.DataFrame(
            {
                "timestamp": [
                    datetime(2023, 12, 23, 10, 0, 0),
                    datetime(2023, 12, 23, 10, 1, 0),
                    datetime(2023, 12, 23, 10, 2, 0),
                ],
                "bid": [1.1000, 1.1001, 1.1002],
                "ask": [1.1002, 1.1003, 1.1004],
                "volume": [1000, 1200, 1100],
                "source": ["jforex", "jforex", "jforex"],
            }
        )

    @pytest.fixture
    def mock_hardware_with_avx2(self) -> MagicMock:
        """Mockolt HardwareInterface AVX2 támogatással."""
        hardware = MagicMock()
        hardware.has_avx2.return_value = True
        return hardware

    @pytest.fixture
    def mock_hardware_without_avx2(self) -> MagicMock:
        """Mockolt HardwareInterface AVX2 támogatás nélkül."""
        hardware = MagicMock()
        hardware.has_avx2.return_value = False
        return hardware

    def test_init_with_avx2_support(self, temp_dir: Path, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli a PolarsBackend kiválasztását AVX2 támogatás esetén."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        assert service.engine == "polars"
        assert service.backend.name == "polars"
        mock_hardware_with_avx2.has_avx2.assert_called_once()

    def test_init_without_avx2_support(self, temp_dir: Path, mock_hardware_without_avx2: MagicMock) -> None:
        """Teszteli a PandasBackend kiválasztását AVX2 támogatás hiányában."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_without_avx2
        )
        
        assert service.engine == "fastparquet"
        assert service.backend.name == "pandas"
        mock_hardware_without_avx2.has_avx2.assert_called_once()

    def test_get_path(self, temp_dir: Path, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli az elérési út generálást."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        date = datetime(2023, 12, 23)
        path = service._get_path("EURUSD", date)
        
        expected_path = (
            service.BASE_PATH / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23" / "data.parquet"
        )
        assert path == expected_path

    @pytest.mark.asyncio
    async def test_store_tick_data_pandas(
        self, temp_dir: Path, mock_hardware_without_avx2: MagicMock, sample_pandas_data: pd.DataFrame
    ) -> None:
        """Teszteli a Pandas DataFrame tárolását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_without_avx2
        )
        
        await service.store_tick_data("EURUSD", sample_pandas_data, datetime(2023, 12, 23))
        
        # Ellenőrizzük, hogy a fájl létrejött-e
        expected_path = (
            temp_dir / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23" / "data.parquet"
        )
        assert expected_path.exists()

    @pytest.mark.asyncio
    async def test_store_tick_data_polars(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a Polars DataFrame tárolását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        
        # Ellenőrizzük, hogy a fájl létrejött-e
        expected_path = (
            temp_dir / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23" / "data.parquet"
        )
        assert expected_path.exists()

    @pytest.mark.asyncio
    async def test_store_empty_dataframe_raises_error(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy üres DataFrame tárolása hibát dob."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        empty_df = pl.DataFrame()
        
        with pytest.raises(ValueError, match="Cannot store empty DataFrame"):
            await service.store_tick_data("EURUSD", empty_df, datetime(2023, 12, 23))

    @pytest.mark.asyncio
    async def test_store_dataframe_missing_columns_raises_error(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy hiányzó oszlopok esetén hiba keletkezik."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        # Csak timestamp oszlop, hiányzik bid és ask
        incomplete_df = pl.DataFrame({"timestamp": [datetime.now()]})
        
        with pytest.raises(ValueError, match="Missing required columns"):
            await service.store_tick_data("EURUSD", incomplete_df, datetime(2023, 12, 23))

    @pytest.mark.asyncio
    async def test_read_tick_data_polars(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a Polars DataFrame olvasását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        # Adatok tárolása
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        
        # Adatok olvasása
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23), datetime(2023, 12, 23)
        )
        
        assert len(result) == 3
        assert "timestamp" in result.columns
        assert "bid" in result.columns
        assert "ask" in result.columns

    @pytest.mark.asyncio
    async def test_read_tick_data_pandas(
        self, temp_dir: Path, mock_hardware_without_avx2: MagicMock, sample_pandas_data: pd.DataFrame
    ) -> None:
        """Teszteli a Pandas DataFrame olvasását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_without_avx2
        )
        
        # Adatok tárolása
        await service.store_tick_data("EURUSD", sample_pandas_data, datetime(2023, 12, 23))
        
        # Adatok olvasása
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23), datetime(2023, 12, 23)
        )
        
        assert len(result) == 3
        assert "timestamp" in result.columns
        assert "bid" in result.columns
        assert "ask" in result.columns

    @pytest.mark.asyncio
    async def test_read_tick_data_multiple_days(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a több napos adatok olvasását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        # Adatok tárolása több napra
        for day in range(23, 26):
            await service.store_tick_data(
                "EURUSD", sample_polars_data, datetime(2023, 12, day)
            )
        
        # Adatok olvasása dátumtartományból
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23), datetime(2023, 12, 25)
        )
        
        assert len(result) == 9  # 3 nap × 3 sor

    @pytest.mark.asyncio
    async def test_read_tick_data_no_data(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli az olvasást, ha nincs adat."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23), datetime(2023, 12, 25)
        )
        
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_available_dates(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli az elérhető dátumok lekérdezését."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        # Adatok tárolása több napra
        dates = [datetime(2023, 12, 23), datetime(2023, 12, 24), datetime(2023, 12, 25)]
        for date in dates:
            await service.store_tick_data("EURUSD", sample_polars_data, date)
        
        # Elérhető dátumok lekérdezése
        available_dates = await service.get_available_dates("EURUSD")
        
        assert len(available_dates) == 3
        assert available_dates == dates

    @pytest.mark.asyncio
    async def test_get_available_dates_no_data(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli az elérhető dátumok lekérdezését, ha nincs adat."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        available_dates = await service.get_available_dates("EURUSD")
        
        assert len(available_dates) == 0

    @pytest.mark.asyncio
    async def test_calculate_checksum(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a checksum számítást."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        
        checksum = await service.calculate_checksum("EURUSD", datetime(2023, 12, 23))
        
        assert len(checksum) == 64  # SHA256 hash hossza
        assert checksum != ""

    @pytest.mark.asyncio
    async def test_calculate_checksum_no_file(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli a checksum számítást, ha nincs fájl."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        checksum = await service.calculate_checksum("EURUSD", datetime(2023, 12, 23))
        
        assert checksum == ""

    @pytest.mark.asyncio
    async def test_verify_data_integrity_success(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli az adatintegritás ellenőrzését sikeres esetben."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        
        is_valid = await service.verify_data_integrity("EURUSD", datetime(2023, 12, 23))
        
        assert is_valid is True

    @pytest.mark.asyncio
    async def test_verify_data_integrity_no_file(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli az adatintegritás ellenőrzését, ha nincs fájl."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        is_valid = await service.verify_data_integrity("EURUSD", datetime(2023, 12, 23))
        
        assert is_valid is False

    @pytest.mark.asyncio
    async def test_get_storage_stats(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a tárolási statisztikák lekérdezését."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        # Adatok tárolása több szimbólumra
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        await service.store_tick_data("GBPUSD", sample_polars_data, datetime(2023, 12, 23))
        
        # Statisztikák lekérdezése
        stats = await service.get_storage_stats()
        
        assert stats["total_files"] == 2
        assert stats["total_size_gb"] > 0
        assert "EURUSD" in stats["symbols"]
        assert "GBPUSD" in stats["symbols"]

    @pytest.mark.asyncio
    async def test_get_storage_stats_with_symbol(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a tárolási statisztikák lekérdezését szimbólum szerint."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        # Adatok tárolása több szimbólumra
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        await service.store_tick_data("GBPUSD", sample_polars_data, datetime(2023, 12, 23))
        
        # Statisztikák lekérdezése csak EURUSD-ra
        stats = await service.get_storage_stats("EURUSD")
        
        assert stats["total_files"] == 1
        assert "EURUSD" in stats["symbols"]
        assert "GBPUSD" not in stats["symbols"]

    @pytest.mark.asyncio
    async def test_singleton_pattern(self, temp_dir: Path, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli a Singleton mintát."""
        service1 = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        service2 = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_with_avx2
        )
        
        assert service1 is service2

    def test_compression_parameter(self, temp_dir: Path, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli a tömörítési paraméter beállítását."""
        service = ParquetStorageService(
            base_path=str(temp_dir),
            compression="gzip",
            hardware=mock_hardware_with_avx2
        )
        
        assert service.compression == "gzip"

    def test_default_base_path(self, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli az alapértelmezett útvonal beállítását."""
        service = ParquetStorageService(hardware=mock_hardware_with_avx2)
        
        assert service.BASE_PATH == Path("/data/tick")