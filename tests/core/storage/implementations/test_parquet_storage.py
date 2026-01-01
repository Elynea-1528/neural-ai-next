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

    def setup_method(self) -> None:
        """Teszt metódus előtti beállítás - Singleton cache törlése."""
        from neural_ai.core.base.implementations.singleton import SingletonMeta

        SingletonMeta._instances.clear()

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

    def test_init_with_avx2_support(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli a PolarsBackend kiválasztását AVX2 támogatás esetén."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        assert service.engine == "polars"
        assert service.backend.name == "polars"
        # A has_avx2-t többször is meghívhatják (pl. inicializáláskor és logoláskor)
        assert mock_hardware_with_avx2.has_avx2.called

    def test_init_without_avx2_support(
        self, temp_dir: Path, mock_hardware_without_avx2: MagicMock
    ) -> None:
        """Teszteli a PandasBackend kiválasztását AVX2 támogatás hiányában."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_without_avx2
        )

        assert service.engine == "fastparquet"
        assert service.backend.name == "pandas"
        # A has_avx2-t többször is meghívhatják (pl. inicializáláskor és logoláskor)
        assert mock_hardware_without_avx2.has_avx2.called

    def test_get_path(self, temp_dir: Path, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli az elérési út generálást egyedi fájlnévvel."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)
        date = datetime(2023, 12, 23)
        path = service._get_path("EURUSD", date)

        # Az elérési útnak tartalmaznia kell a dátumot és egy UUID-t
        expected_dir = service.BASE_PATH / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23"
        assert path.parent == expected_dir
        assert path.name.startswith("tick_20231223_")
        assert path.name.endswith(".parquet")
        assert len(path.name) == len("tick_20231223_") + 8 + len(".parquet")  # 8 karakteres UUID

    @pytest.mark.skip(reason="FastParquet kompatibilitási hiba Pandas/NumPy kombinációval")
    @pytest.mark.asyncio
    async def test_store_tick_data_pandas(
        self,
        temp_dir: Path,
        mock_hardware_without_avx2: MagicMock,
        sample_pandas_data: pd.DataFrame,
    ) -> None:
        """Teszteli a Pandas DataFrame tárolását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_without_avx2
        )

        await service.store_tick_data("EURUSD", sample_pandas_data, datetime(2023, 12, 23))

        # Ellenőrizzük, hogy a fájl létrejött-e egyedi névvel
        expected_dir = temp_dir / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23"
        assert expected_dir.exists()

        # Ellenőrizzük, hogy van-e Parquet fájl a mappában
        parquet_files = list(expected_dir.glob("*.parquet"))
        assert len(parquet_files) == 1
        assert parquet_files[0].name.startswith("tick_20231223_")
        assert parquet_files[0].name.endswith(".parquet")

    @pytest.mark.asyncio
    async def test_store_tick_data_polars(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a Polars DataFrame tárolását."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))

        # Ellenőrizzük, hogy a fájl létrejött-e egyedi névvel
        expected_dir = temp_dir / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23"
        assert expected_dir.exists()

        # Ellenőrizzük, hogy van-e Parquet fájl a mappában
        parquet_files = list(expected_dir.glob("*.parquet"))
        assert len(parquet_files) == 1
        assert parquet_files[0].name.startswith("tick_20231223_")
        assert parquet_files[0].name.endswith(".parquet")

    @pytest.mark.asyncio
    async def test_store_empty_dataframe_raises_error(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy üres DataFrame tárolása hibát dob."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        empty_df = pl.DataFrame()

        with pytest.raises(ValueError, match="Cannot store empty DataFrame"):
            await service.store_tick_data("EURUSD", empty_df, datetime(2023, 12, 23))

    @pytest.mark.asyncio
    async def test_store_dataframe_missing_columns_raises_error(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy hiányzó oszlopok esetén hiba keletkezik."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Csak timestamp oszlop, hiányzik bid és ask
        incomplete_df = pl.DataFrame({"timestamp": [datetime.now()]})

        with pytest.raises(ValueError, match="Missing required columns"):
            await service.store_tick_data("EURUSD", incomplete_df, datetime(2023, 12, 23))

    @pytest.mark.asyncio
    async def test_read_tick_data_polars(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a Polars DataFrame olvasását."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Adatok tárolása
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))

        # Adatok olvasása
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23, 0, 0, 0), datetime(2023, 12, 23, 23, 59, 59)
        )

        assert len(result) == 3
        assert "timestamp" in result.columns
        assert "bid" in result.columns
        assert "ask" in result.columns

    @pytest.mark.skip(reason="FastParquet kompatibilitási hiba Pandas/NumPy kombinációval")
    @pytest.mark.asyncio
    async def test_read_tick_data_pandas(
        self,
        temp_dir: Path,
        mock_hardware_without_avx2: MagicMock,
        sample_pandas_data: pd.DataFrame,
    ) -> None:
        """Teszteli a Pandas DataFrame olvasását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), hardware=mock_hardware_without_avx2
        )

        # Adatok tárolása
        await service.store_tick_data("EURUSD", sample_pandas_data, datetime(2023, 12, 23))

        # Adatok olvasása
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23, 0, 0, 0), datetime(2023, 12, 23, 23, 59, 59)
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
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Adatok tárolása több napra
        for day in range(23, 26):
            await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, day))

        # Adatok olvasása dátumtartományból
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23), datetime(2023, 12, 25)
        )

        assert (
            len(result) == 3
        )  # 3 nap × 3 sor, de deduplikálva (mivel minden nap ugyanazok az adatok)
        # A deduplikáció miatt csak az egyedi timestamp-ek maradnak meg

    @pytest.mark.asyncio
    async def test_read_tick_data_no_data(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli az olvasást, ha nincs adat."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23), datetime(2023, 12, 25)
        )

        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_available_dates(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli az elérhető dátumok lekérdezését."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

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
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        available_dates = await service.get_available_dates("EURUSD")

        assert len(available_dates) == 0

    @pytest.mark.asyncio
    async def test_calculate_checksum(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a checksum számítást."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))

        checksum = await service.calculate_checksum("EURUSD", datetime(2023, 12, 23))

        assert len(checksum) == 64  # SHA256 hash hossza
        assert checksum != ""

    @pytest.mark.asyncio
    async def test_calculate_checksum_no_file(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli a checksum számítást, ha nincs fájl."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        checksum = await service.calculate_checksum("EURUSD", datetime(2023, 12, 23))

        assert checksum == ""

    @pytest.mark.asyncio
    async def test_verify_data_integrity_success(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli az adatintegritás ellenőrzését sikeres esetben."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))

        is_valid = await service.verify_data_integrity("EURUSD", datetime(2023, 12, 23))

        assert is_valid is True

    @pytest.mark.asyncio
    async def test_verify_data_integrity_no_file(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli az adatintegritás ellenőrzését, ha nincs fájl."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        is_valid = await service.verify_data_integrity("EURUSD", datetime(2023, 12, 23))

        assert is_valid is False

    @pytest.mark.asyncio
    async def test_get_storage_stats(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a tárolási statisztikák lekérdezését."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Adatok tárolása több szimbólumra
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        await service.store_tick_data("GBPUSD", sample_polars_data, datetime(2023, 12, 23))

        # Statisztikák lekérdezése
        stats = await service.get_storage_stats()

        assert stats["total_files"] == 2
        assert stats["total_size_gb"] > 0
        assert "symbols" in stats
        assert "EURUSD" in stats["symbols"]
        assert "GBPUSD" in stats["symbols"]
        assert stats["symbols"]["EURUSD"]["files"] == 1
        assert stats["symbols"]["GBPUSD"]["files"] == 1

    @pytest.mark.asyncio
    async def test_get_storage_stats_with_symbol(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a tárolási statisztikák lekérdezését szimbólum szerint."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Adatok tárolása több szimbólumra
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        await service.store_tick_data("GBPUSD", sample_polars_data, datetime(2023, 12, 23))

        # Statisztikák lekérdezése csak EURUSD-ra
        stats = await service.get_storage_stats("EURUSD")

        assert stats["total_files"] == 1
        assert "symbols" in stats
        assert "tick" in stats["symbols"]
        assert stats["symbols"]["tick"]["files"] == 1
        assert stats["symbols"]["tick"]["size_gb"] > 0

    @pytest.mark.asyncio
    async def test_singleton_pattern(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli a Singleton mintát."""
        service1 = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)
        service2 = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        assert service1 is service2

    def test_compression_parameter(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli a tömörítési paraméter beállítását."""
        service = ParquetStorageService(
            base_path=str(temp_dir), compression="gzip", hardware=mock_hardware_with_avx2
        )

        assert service.compression == "gzip"

    def test_default_base_path(self, mock_hardware_with_avx2: MagicMock) -> None:
        """Teszteli az alapértelmezett útvonal beállítását."""
        service = ParquetStorageService(hardware=mock_hardware_with_avx2)

        assert service.BASE_PATH == Path("/data/tick")

    @pytest.mark.asyncio
    async def test_store_multiple_files_same_day(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli, hogy több fájl is létrejöhet egy napon (nem írja felül a régit)."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Két fájl tárolása ugyanarra a napra
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))

        # Ellenőrizzük, hogy két fájl van-e a mappában
        expected_dir = temp_dir / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23"
        parquet_files = list(expected_dir.glob("*.parquet"))
        assert len(parquet_files) == 2

    @pytest.mark.asyncio
    async def test_read_with_deduplication(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock, sample_polars_data: pl.DataFrame
    ) -> None:
        """Teszteli a deduplikációt olvasáskor."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Két azonos adatokat tartalmazó fájl tárolása
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))
        await service.store_tick_data("EURUSD", sample_polars_data, datetime(2023, 12, 23))

        # Adatok olvasása (deduplikációval)
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23, 0, 0, 0), datetime(2023, 12, 23, 23, 59, 59)
        )

        # Ellenőrizzük, hogy a duplikátumok el lettek-e távolítva
        assert len(result) == 3  # Csak az eredeti 3 sor marad
        assert "timestamp" in result.columns
        assert "bid" in result.columns
        assert "ask" in result.columns

    @pytest.mark.asyncio
    async def test_read_with_sorting(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli a rendezettséget olvasáskor."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

        # Adatok létrehozása fordított sorrendben
        reversed_data = pl.DataFrame(
            {
                "timestamp": [
                    datetime(2023, 12, 23, 10, 2, 0),
                    datetime(2023, 12, 23, 10, 1, 0),
                    datetime(2023, 12, 23, 10, 0, 0),
                ],
                "bid": [1.1002, 1.1001, 1.1000],
                "ask": [1.1004, 1.1003, 1.1002],
                "volume": [1100, 1200, 1000],
                "source": ["jforex", "jforex", "jforex"],
            }
        )

        await service.store_tick_data("EURUSD", reversed_data, datetime(2023, 12, 23))

        # Adatok olvasása
        result = await service.read_tick_data(
            "EURUSD", datetime(2023, 12, 23, 0, 0, 0), datetime(2023, 12, 23, 23, 59, 59)
        )

        # Ellenőrizzük, hogy rendezve vannak-e az adatok
        timestamps = result["timestamp"].to_list()
        assert timestamps == sorted(timestamps)


class TestParquetStorageAdapterMethods:
    """ParquetStorage adapter metódusok tesztek (StorageInterface)."""

    def setup_method(self) -> None:
        """Teszt metódus előtti beállítás - Singleton cache törlése."""
        from neural_ai.core.base.implementations.singleton import SingletonMeta

        SingletonMeta._instances.clear()

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Ideiglenes könyvtár létrehozása a tesztekhez."""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        shutil.rmtree(tmpdir)

    @pytest.fixture
    def mock_hardware_with_avx2(self) -> MagicMock:
        """Mockolt HardwareInterface AVX2 támogatással."""
        hardware = MagicMock()
        hardware.has_avx2.return_value = True
        return hardware

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
                "source": ["jforex", "jforex", "jforex"],
            }
        )

    @pytest.fixture
    def storage_service(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> ParquetStorageService:
        """ParquetStorageService példány létrehozása."""
        return ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)

    def test_adapter_save_object(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a save_object adapter metódust."""
        test_obj = {"key": "value", "number": 42}
        storage_service.save_object(test_obj, "test_object.pkl")

        # Ellenőrizzük, hogy létrejött-e a fájl
        assert storage_service.exists("test_object.pkl")

    def test_adapter_load_object(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a load_object adapter metódust."""
        test_obj = {"key": "value", "number": 42}
        storage_service.save_object(test_obj, "test_object.pkl")

        loaded = storage_service.load_object("test_object.pkl")
        assert loaded == test_obj

    def test_adapter_exists(self, storage_service: ParquetStorageService) -> None:
        """Teszteli az exists adapter metódust."""
        # Először nem létezik
        assert not storage_service.exists("test_exists.txt")

        # Hozzunk létre egy fájlt
        storage_service.save_object({"test": "data"}, "test_exists.pkl")
        assert storage_service.exists("test_exists.pkl")

    def test_adapter_delete(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a delete adapter metódust."""
        # Hozzunk létre egy fájlt
        storage_service.save_object({"test": "data"}, "test_delete.pkl")
        assert storage_service.exists("test_delete.pkl")

        # Töröljük
        storage_service.delete("test_delete.pkl")
        assert not storage_service.exists("test_delete.pkl")

    def test_adapter_get_metadata(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a get_metadata adapter metódust."""
        storage_service.save_object({"test": "data"}, "test_metadata.pkl")

        metadata = storage_service.get_metadata("test_metadata.pkl")
        assert "size" in metadata
        assert "is_file" in metadata
        assert metadata["is_file"] is True

    def test_adapter_list_dir(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a list_dir adapter metódust."""
        # Hozzunk létre néhány fájlt
        storage_service.save_object({"test": "data1"}, "dir1/file1.pkl")
        storage_service.save_object({"test": "data2"}, "dir1/file2.pkl")

        files = storage_service.list_dir("dir1")
        assert len(files) == 2
        filenames = [f.name for f in files]
        assert "file1.pkl" in filenames
        assert "file2.pkl" in filenames

    def test_smart_filename_uniqueness(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy a _get_path egyedi fájlneveket generál."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)
        date = datetime(2023, 12, 23)

        # Generáljunk több fájlnevet ugyanarra a napra
        paths = []
        for _ in range(10):
            path = service._get_path("EURUSD", date)
            paths.append(path)

        # Ellenőrizzük, hogy minden név egyedi
        filenames = [p.name for p in paths]
        assert len(set(filenames)) == len(filenames)  # Minden név egyedi

        # Ellenőrizzük a formátumot
        for filename in filenames:
            assert filename.startswith("tick_20231223_")
            assert filename.endswith(".parquet")
            # UUID rész 8 karakter hosszú
            uuid_part = filename.split("_")[-1].replace(".parquet", "")
            assert len(uuid_part) == 8
            assert uuid_part.isalnum()  # Csak alfanumerikus karakterek

    def test_adapter_save_object_with_nested_path(
        self, storage_service: ParquetStorageService
    ) -> None:
        """Teszteli a save_object adapter metódust beágyazott útvonallal."""
        test_obj = {"key": "nested", "value": 123}
        storage_service.save_object(test_obj, "subdir/nested/test_object.pkl")

        # Ellenőrizzük, hogy létrejött-e a fájl a beágyazott útvonalon
        assert storage_service.exists("subdir/nested/test_object.pkl")

    def test_adapter_load_object_not_found(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a load_object hibakezelését, ha a fájl nem létezik."""
        # Nem létező fájl betöltése hibát okoz
        with pytest.raises(FileNotFoundError):
            storage_service.load_object("nonexistent.pkl")

    def test_adapter_exists_for_directory(self, storage_service: ParquetStorageService) -> None:
        """Teszteli az exists metódust könyvtárra."""
        # Könyvtár létezésének ellenőrzése
        storage_service.save_object({"test": "data"}, "test_dir/file.pkl")
        assert storage_service.exists("test_dir")

    def test_adapter_delete_directory(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a delete metódust könyvtárra."""
        # Könyvtár létrehozása fájllal
        storage_service.save_object({"test": "data"}, "delete_dir/file.pkl")
        assert storage_service.exists("delete_dir")

        # Könyvtár törlése
        storage_service.delete("delete_dir")
        assert not storage_service.exists("delete_dir")

    def test_adapter_delete_not_found(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a delete hibakezelését, ha a fájl nem létezik."""
        from neural_ai.core.storage.exceptions import StorageNotFoundError

        # Nem létező fájl törlése hibát okoz
        with pytest.raises(StorageNotFoundError):
            storage_service.delete("nonexistent.pkl")

    def test_adapter_get_metadata_for_directory(
        self, storage_service: ParquetStorageService
    ) -> None:
        """Teszteli a get_metadata metódust könyvtárra."""
        storage_service.save_object({"test": "data"}, "metadata_dir/file.pkl")

        metadata = storage_service.get_metadata("metadata_dir")
        assert "size" in metadata
        assert "is_dir" in metadata
        assert metadata["is_dir"] is True

    def test_adapter_get_metadata_not_found(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a get_metadata hibakezelését, ha a fájl nem létezik."""
        from neural_ai.core.storage.exceptions import StorageNotFoundError

        # Nem létező fájl metaadatainak lekérdezése hibát okoz
        with pytest.raises(StorageNotFoundError):
            storage_service.get_metadata("nonexistent.pkl")

    def test_adapter_list_dir_with_pattern(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a list_dir metódust glob patternmel."""
        # Hozzunk létre néhány fájlt
        storage_service.save_object({"test": "data1"}, "pattern_dir/file1.pkl")
        storage_service.save_object({"test": "data2"}, "pattern_dir/file2.txt")
        storage_service.save_object({"test": "data3"}, "pattern_dir/file3.pkl")

        # Csak .pkl fájlok listázása
        files = storage_service.list_dir("pattern_dir", pattern="*.pkl")
        assert len(files) == 2
        filenames = [f.name for f in files]
        assert "file1.pkl" in filenames
        assert "file3.pkl" in filenames
        assert "file2.txt" not in filenames

    def test_adapter_list_dir_not_found(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a list_dir hibakezelését, ha a könyvtár nem létezik."""
        from neural_ai.core.storage.exceptions import StorageNotFoundError

        # Nem létező könyvtár listázása hibát okoz
        with pytest.raises(StorageNotFoundError):
            storage_service.list_dir("nonexistent_dir")

    def test_adapter_list_dir_on_file(self, storage_service: ParquetStorageService) -> None:
        """Teszteli a list_dir hibakezelését, ha az útvonal fájl."""
        from neural_ai.core.storage.exceptions import StorageIOError

        # Fájlon való listázás hibát okoz
        storage_service.save_object({"test": "data"}, "list_test/file.pkl")
        with pytest.raises(StorageIOError):
            storage_service.list_dir("list_test/file.pkl")

    def test_smart_filename_with_custom_unique_id(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy a _get_path egyedi azonosítóval generál fájlnevet."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)
        date = datetime(2023, 12, 23)

        # Egyedi azonosítóval generálunk fájlnevet
        custom_id = "custom123"
        path = service._get_path("EURUSD", date, unique_id=custom_id)

        # Ellenőrizzük a formátumot
        assert path.name == f"tick_20231223_{custom_id}.parquet"

    def test_smart_filename_path_structure(
        self, temp_dir: Path, mock_hardware_with_avx2: MagicMock
    ) -> None:
        """Teszteli, hogy a _get_path helyes útvonalszerkezetet generál."""
        service = ParquetStorageService(base_path=str(temp_dir), hardware=mock_hardware_with_avx2)
        date = datetime(2023, 12, 23)

        path = service._get_path("EURUSD", date)

        # Ellenőrizzük az útvonalszerkezetet
        assert path.parent.name == "day=23"
        assert path.parent.parent.name == "month=12"
        assert path.parent.parent.parent.name == "year=2023"
        assert path.parent.parent.parent.parent.name == "tick"
        assert path.parent.parent.parent.parent.parent.name == "EURUSD"
        assert path.parent.parent.parent.parent.parent.parent == temp_dir

    def test_adapter_save_dataframe_sync(
        self, storage_service: ParquetStorageService, sample_pandas_data: pd.DataFrame
    ) -> None:
        """Teszteli a save_dataframe adapter metódust szinkron hívásra."""
        storage_service.save_dataframe(
            sample_pandas_data,
            "test_dataframe.parquet",
            symbol="EURUSD",
            date=datetime(2023, 12, 23),
        )

        # Ellenőrizzük, hogy létrejött-e a fájl
        date_dir = (
            storage_service.BASE_PATH / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23"
        )
        assert date_dir.exists()
        parquet_files = list(date_dir.glob("*.parquet"))
        assert len(parquet_files) >= 1

    def test_adapter_load_dataframe_sync(
        self, storage_service: ParquetStorageService, sample_pandas_data: pd.DataFrame
    ) -> None:
        """Teszteli a load_dataframe adapter metódust szinkron hívásra."""
        # Először mentünk egy DataFrame-et
        storage_service.save_dataframe(
            sample_pandas_data,
            "test_dataframe.parquet",
            symbol="EURUSD",
            date=datetime(2023, 12, 23),
        )

        # Majd betöltjük
        result = storage_service.load_dataframe(
            "test_dataframe.parquet",
            symbol="EURUSD",
            start_date=datetime(2023, 12, 23),
            end_date=datetime(2023, 12, 23, 23, 59, 59),
        )

        # Ellenőrizzük az eredményt
        assert len(result) == 3
        assert "timestamp" in result.columns
        assert "bid" in result.columns
        assert "ask" in result.columns
