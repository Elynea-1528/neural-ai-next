"""ParquetStorageService tesztesetek - teljes lefedettséget biztosít.

Ez a modul tartalmazza a ParquetStorageService osztály minden metódusának
egységtesztjeit, biztosítva a 100% kódlefedettséget.

Author: Neural AI Next Team
Version: 2.0.0
"""

import asyncio
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService


@pytest.fixture(scope="function")
def temp_dir():
    """Ideiglenes könyvtár fixture."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture(scope="function")
def mock_hardware():
    """Mock HardwareInterface fixture."""
    hardware: MagicMock = MagicMock()
    hardware.has_avx2.return_value = True
    return hardware


@pytest.fixture(scope="function")
def mock_logger() -> MagicMock:
    """Mock LoggerInterface fixture."""
    return MagicMock()


@pytest.fixture(autouse=True)
def clear_singletons():
    """Singleton példányok törlése minden teszt előtt."""
    from neural_ai.core.base.implementations.singleton import SingletonMeta

    SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]
    yield
    SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]


@pytest.fixture(scope="function")
async def storage_service(temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock):
    """ParquetStorageService fixture teljes mock konfigurációval."""
    service = ParquetStorageService(
        logger=mock_logger,
        config=None,
        event_bus=None,
        base_path=str(temp_dir),
        compression="snappy",
        hardware=mock_hardware,
    )
    return service


class TestParquetStorageService:
    """ParquetStorageService osztály tesztesetek."""

    @pytest.mark.asyncio
    async def test_initialization_with_hardware_and_logger(
        self, temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock
    ):
        """Teszteli az inicializációt hardware és logger interfészekkel."""
        mock_config: MagicMock = MagicMock()
        mock_config.get_section.return_value = {}

        service = ParquetStorageService(
            logger=mock_logger,
            config=mock_config,
            event_bus=None,
            base_path=str(temp_dir),
            compression="snappy",
            hardware=mock_hardware,
        )

        assert service.base_path == temp_dir
        assert service.compression == "snappy"
        assert service.hardware == mock_hardware
        assert service.logger == mock_logger

    @pytest.mark.asyncio
    async def test_initialization_without_hardware_and_logger(self, temp_dir: Path):
        """Teszteli az inicializációt factory-k használatával."""
        with patch("neural_ai.core.utils.factory.HardwareFactory") as mock_factory:
            mock_factory.get_hardware_interface.return_value = MagicMock()
            mock_factory.get_hardware_interface.return_value.has_avx2.return_value = False

            mock_logger: MagicMock = MagicMock()

            # Mock config to avoid Pydantic validation error if it tries to access it
            service = ParquetStorageService(
                base_path=str(temp_dir), config=None, logger=mock_logger
            )

            assert service.base_path == temp_dir
            mock_factory.get_hardware_interface.assert_called_once()

    def test_backend_selection_avx2(
        self, temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock
    ):
        """Teszteli a PolarsBackend kiválasztását AVX2 támogatással."""
        mock_hardware.has_avx2.return_value = True

        with patch("neural_ai.data.storage.backends.polars_backend.PolarsBackend") as mock_backend:
            service = ParquetStorageService(
                base_path=str(temp_dir),
                hardware=mock_hardware,
                logger=mock_logger,
            )

            mock_backend.assert_called_once()
            assert service.engine == "polars"
            mock_logger.info.assert_called()

    def test_backend_selection_no_avx2(
        self, temp_dir: Path, mock_hardware: MagicMock, mock_logger: MagicMock
    ):
        """Teszteli a PandasBackend kiválasztását AVX2 nélkül."""
        mock_hardware.has_avx2.return_value = False

        with patch("neural_ai.data.storage.backends.pandas_backend.PandasBackend") as mock_backend:
            service = ParquetStorageService(
                base_path=str(temp_dir),
                hardware=mock_hardware,
                logger=mock_logger,
            )

            mock_backend.assert_called_once()
            assert service.engine == "fastparquet"
            mock_logger.warning.assert_called()

    def test_get_path_with_unique_id(self, storage_service: ParquetStorageService):
        """Teszteli az elérési út generálást egyedi azonosítóval."""
        date = datetime(2023, 12, 23)
        path = storage_service._get_path("EURUSD", date, unique_id="abc123")  # pyright: ignore[reportPrivateUsage]

        expected = (
            storage_service.base_path
            / "EURUSD"
            / "year=2023"
            / "month=12"
            / "day=23"
            / "tick_20231223_abc123.parquet"
        )
        assert path == expected

    def test_get_path_without_unique_id(self, storage_service: ParquetStorageService):
        """Teszteli az elérési út generálást időbélyeggel."""
        date = datetime(2023, 12, 23)

        mock_now = MagicMock()
        mock_now.strftime.return_value = "123045_123456"

        with patch(
            "neural_ai.data.storage.implementations.parquet_storage.datetime"
        ) as mock_datetime:
            mock_datetime.now.return_value = mock_now

            path = storage_service._get_path("EURUSD", date)  # pyright: ignore[reportPrivateUsage]

            assert "tick_20231223_123045_123456.parquet" in str(path)

    @pytest.mark.asyncio
    async def test_store_tick_data_success(
        self, storage_service: ParquetStorageService, mock_logger: MagicMock
    ):
        """Teszteli a tick adatok sikeres tárolását."""
        date = datetime(2023, 12, 23)

        # Mock DataFrame
        mock_df: MagicMock = MagicMock()
        mock_df.columns = ["timestamp", "bid", "ask", "volume"]
        mock_df.__len__ = MagicMock(return_value=100)

        # Mock backend
        storage_service.backend.write = MagicMock()  # type: ignore[method-assign]

        # Mock path.stat to avoid FileNotFoundError
        with patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value = MagicMock(st_size=1024)

            await storage_service.store_tick_data("EURUSD", mock_df, date)

            # Ellenőrzi hogy a backend.write meghívódott
            storage_service.backend.write.assert_called_once()

            # Ellenőrzi a loggolást
            mock_logger.info.assert_called()

    @pytest.mark.asyncio
    async def test_store_tick_data_empty_dataframe(self, storage_service: ParquetStorageService):
        """Teszteli az üres DataFrame visszautasítását."""
        date = datetime(2023, 12, 23)
        mock_df: MagicMock = MagicMock()
        mock_df.__len__ = MagicMock(return_value=0)

        with pytest.raises(ValueError, match="Cannot store empty DataFrame"):
            await storage_service.store_tick_data("EURUSD", mock_df, date)

    @pytest.mark.asyncio
    async def test_store_tick_data_missing_columns(self, storage_service: ParquetStorageService):
        """Teszteli a hiányzó oszlopok visszautasítását."""
        date = datetime(2023, 12, 23)
        mock_df: MagicMock = MagicMock()
        mock_df.columns = ["timestamp", "bid"]  # Hiányzik ask
        mock_df.__len__ = MagicMock(return_value=100)

        with pytest.raises(ValueError, match="Missing required columns"):
            await storage_service.store_tick_data("EURUSD", mock_df, date)

    @pytest.mark.asyncio
    async def test_read_tick_data_no_files(self, storage_service: ParquetStorageService):
        """Teszteli az olvasást amikor nincsenek fájlok."""
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2023, 12, 31)

        result = await storage_service.read_tick_data("EURUSD", start_date, end_date)

        # Üres DataFrame visszaadása
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_read_tick_data_with_files(
        self, storage_service: ParquetStorageService, temp_dir: Path
    ):
        """Teszteli az olvasást létező fájlokkal."""
        start_date = datetime(2023, 12, 23)
        end_date = datetime(2023, 12, 23)

        # Hozz létre egy teszt fájlt
        date_dir = temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=23"
        date_dir.mkdir(parents=True, exist_ok=True)

        test_file = date_dir / "tick_20231223_test.parquet"
        test_file.write_text("dummy parquet content")

        # Mock backend read
        mock_df: MagicMock = MagicMock()
        mock_df.columns = ["timestamp", "bid", "ask"]
        mock_df.__len__ = MagicMock(return_value=50)

        storage_service.backend.read = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._concat_dataframes = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._deduplicate_data = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._sort_by_timestamp = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._filter_by_timestamp = MagicMock(return_value=mock_df)  # type: ignore[method-assign]

        with (
            patch("neural_ai.data.storage.implementations.parquet_storage.pl") as mock_pl,
            patch("neural_ai.data.storage.implementations.parquet_storage.pd") as mock_pd,
        ):
            mock_pl.DataFrame.return_value = mock_df
            mock_pd.DataFrame.return_value = mock_df
            mock_pl.concat.return_value = mock_df
            mock_pd.concat.return_value = mock_df

            result = await storage_service.read_tick_data("EURUSD", start_date, end_date)

            assert result == mock_df

    @pytest.mark.asyncio
    async def test_get_available_dates(
        self, storage_service: ParquetStorageService, temp_dir: Path
    ):
        """Teszteli az elérhető dátumok lekérdezést."""
        # Hozz létre teszt könyvtár struktúrát
        (temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=23").mkdir(parents=True)
        (temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=24").mkdir(parents=True)

        dates = await storage_service.get_available_dates("EURUSD")

        expected_dates = [
            datetime(2023, 12, 23),
            datetime(2023, 12, 24),
        ]
        assert sorted(dates) == sorted(expected_dates)

    @pytest.mark.asyncio
    async def test_get_available_dates_no_symbol(self, storage_service: ParquetStorageService):
        """Teszteli az elérhető dátumokat nem létező szimbólum esetén."""
        dates = await storage_service.get_available_dates("NONEXISTENT")

        assert dates == []

    @pytest.mark.asyncio
    async def test_calculate_checksum_no_files(self, storage_service: ParquetStorageService):
        """Teszteli a checksum számítást amikor nincsenek fájlok."""
        date = datetime(2023, 12, 23)

        checksum = await storage_service.calculate_checksum("EURUSD", date)

        assert checksum == ""

    @pytest.mark.asyncio
    async def test_calculate_checksum_with_files(
        self, storage_service: ParquetStorageService, temp_dir: Path
    ):
        """Teszteli a checksum számítást létező fájlokkal."""
        date = datetime(2023, 12, 23)

        # Hozz létre teszt fájlt
        date_dir = temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=23"
        date_dir.mkdir(parents=True, exist_ok=True)

        test_file = date_dir / "tick_20231223_test.parquet"
        test_file.write_text("dummy")

        # Mock DataFrame és CSV
        mock_df: MagicMock = MagicMock()
        mock_df.select.return_value.write_csv.return_value = "timestamp,bid,ask\n2023-12-23,1.1,1.2"

        storage_service.backend.read = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._concat_dataframes = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._deduplicate_data = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._sort_by_timestamp = MagicMock(return_value=mock_df)  # type: ignore[method-assign]

        with (
            patch.object(storage_service, "engine", "polars"),
            patch("neural_ai.data.storage.implementations.parquet_storage.pl") as mock_pl,
            patch("neural_ai.data.storage.implementations.parquet_storage.pd") as mock_pd,
        ):
            mock_pl.DataFrame.return_value = mock_df
            mock_pd.DataFrame.return_value = mock_df
            mock_pl.concat.return_value = mock_df
            mock_pd.concat.return_value = mock_df

            checksum = await storage_service.calculate_checksum("EURUSD", date)

            assert isinstance(checksum, str)
            assert len(checksum) == 64  # SHA256 hex length

    @pytest.mark.asyncio
    async def test_verify_data_integrity_valid(
        self, storage_service: ParquetStorageService, temp_dir: Path, mock_logger: MagicMock
    ):
        """Teszteli az adat integritás ellenőrzést érvényes adatokkal."""
        date = datetime(2023, 12, 23)

        # Hozz létre teszt fájlt
        date_dir = temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=23"
        date_dir.mkdir(parents=True, exist_ok=True)

        test_file = date_dir / "tick_20231223_test.parquet"
        test_file.write_text("dummy")

        # Mock DataFrame
        mock_df: MagicMock = MagicMock()
        mock_df.columns = ["timestamp", "bid", "ask", "volume", "source"]
        mock_df.__len__ = MagicMock(return_value=50)

        storage_service.backend.read = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._concat_dataframes = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._deduplicate_data = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._sort_by_timestamp = MagicMock(return_value=mock_df)  # type: ignore[method-assign]

        with (
            patch.object(storage_service, "engine", "pandas"),
            patch("neural_ai.data.storage.implementations.parquet_storage.pl") as mock_pl,
            patch("neural_ai.data.storage.implementations.parquet_storage.pd") as mock_pd,
        ):
            mock_pl.DataFrame.return_value = mock_df
            mock_pd.DataFrame.return_value = mock_df
            mock_pl.concat.return_value = mock_df
            mock_pd.concat.return_value = mock_df
            mock_df.is_monotonic_increasing = True

            result = await storage_service.verify_data_integrity("EURUSD", date)

            assert result is True
            mock_logger.info.assert_called()

    @pytest.mark.asyncio
    async def test_verify_data_integrity_no_files(self, storage_service: ParquetStorageService):
        """Teszteli az adat integritás ellenőrzést hiányzó fájlok esetén."""
        date = datetime(2023, 12, 23)

        result = await storage_service.verify_data_integrity("EURUSD", date)

        assert result is False

    @pytest.mark.asyncio
    async def test_verify_data_integrity_missing_columns(
        self, storage_service: ParquetStorageService, temp_dir: Path
    ):
        """Teszteli az adat integritás ellenőrzést hiányzó oszlopokkal."""
        date = datetime(2023, 12, 23)

        # Hozz létre teszt fájlt
        date_dir = temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=23"
        date_dir.mkdir(parents=True, exist_ok=True)

        test_file = date_dir / "tick_20231223_test.parquet"
        test_file.write_text("dummy")

        # Mock DataFrame hiányzó timestamp oszloppal
        mock_df: MagicMock = MagicMock()
        mock_df.columns = ["bid", "ask"]

        storage_service.backend.read = MagicMock(return_value=mock_df)  # type: ignore[method-assign]
        storage_service._concat_dataframes = MagicMock(return_value=mock_df)  # type: ignore[method-assign]

        result = await storage_service.verify_data_integrity("EURUSD", date)

        assert result is False

    @pytest.mark.asyncio
    async def test_get_storage_stats(self, storage_service: ParquetStorageService, temp_dir: Path):
        """Teszteli a tárolási statisztikák lekérdezést."""
        # Hozz létre teszt fájlokat
        test_file1 = (
            temp_dir / "EURUSD" / "year=2023" / "month=12" / "day=23" / "tick_20231223_1.parquet"
        )
        test_file2 = (
            temp_dir / "USDJPY" / "year=2023" / "month=12" / "day=24" / "tick_20231224_2.parquet"
        )

        test_file1.parent.mkdir(parents=True, exist_ok=True)
        test_file2.parent.mkdir(parents=True, exist_ok=True)

        test_file1.write_text("dummy content 1")
        test_file2.write_text("dummy content 2")

        stats = await storage_service.get_storage_stats()

        assert stats["total_files"] == 2
        assert "total_size_gb" in stats
        assert "symbols" in stats
        assert "EURUSD" in stats["symbols"]
        assert "USDJPY" in stats["symbols"]

    def test_concat_dataframes_polars(self, storage_service: ParquetStorageService):
        """Teszteli a DataFrame összefűzést Polars esetén."""
        mock_df1: MagicMock = MagicMock()
        mock_df2: MagicMock = MagicMock()
        mock_concat_result: MagicMock = MagicMock()

        # Patching polars.concat directly as it is imported inside the method
        with patch("polars.concat", return_value=mock_concat_result) as mock_concat:
            with patch.object(storage_service, "engine", "polars"):
                result = storage_service._concat_dataframes([mock_df1, mock_df2])  # pyright: ignore[reportPrivateUsage]

                assert result == mock_concat_result
                mock_concat.assert_called_once_with([mock_df1, mock_df2])

    def test_concat_dataframes_pandas(self, storage_service: ParquetStorageService):
        """Teszteli a DataFrame összefűzést Pandas esetén."""
        mock_df1: MagicMock = MagicMock()
        mock_df2: MagicMock = MagicMock()
        mock_concat_result: MagicMock = MagicMock()

        # Patching pandas.concat directly as it is imported inside the method
        with patch("pandas.concat", return_value=mock_concat_result) as mock_concat:
            with patch.object(storage_service, "engine", "fastparquet"):
                result = storage_service._concat_dataframes([mock_df1, mock_df2])  # pyright: ignore[reportPrivateUsage]

                assert result == mock_concat_result
                mock_concat.assert_called_once_with([mock_df1, mock_df2], ignore_index=True)

    def test_deduplicate_data_polars(self, storage_service: ParquetStorageService):
        """Teszteli a deduplikációt Polars esetén."""
        with patch("neural_ai.data.storage.implementations.parquet_storage.pl"):
            mock_df: MagicMock = MagicMock()
            mock_df.columns = ["timestamp", "bid", "ask"]
            mock_df.select.return_value.unique.return_value = mock_df

            with patch.object(storage_service, "engine", "polars"):
                result = storage_service._deduplicate_data(mock_df)  # pyright: ignore[reportPrivateUsage]

                assert result == mock_df

    def test_deduplicate_data_pandas(self, storage_service: ParquetStorageService):
        """Teszteli a deduplikációt Pandas esetén."""
        mock_df: MagicMock = MagicMock()
        mock_df.columns = ["timestamp", "bid", "ask"]
        # Mocking subset selection result
        mock_subset: MagicMock = MagicMock()
        mock_df.__getitem__.return_value = mock_subset

        mock_dedup_result: MagicMock = MagicMock()
        mock_subset.drop_duplicates.return_value = mock_dedup_result

        # Create a mock data object that has to_pandas method
        mock_data: MagicMock = MagicMock()
        mock_data.to_pandas.return_value = mock_df

        with patch.object(storage_service, "engine", "fastparquet"):
            # Mocking pandas module import inside the method is hard, but we don't need to
            # if we trigger to_pandas path.
            # However, we still need pandas to be importable.

            result = storage_service._deduplicate_data(mock_data)  # pyright: ignore[reportPrivateUsage]
            assert result == mock_dedup_result

    def test_sort_by_timestamp_polars(self, storage_service: ParquetStorageService):
        """Teszteli a rendezést timestamp szerint Polars esetén."""
        with patch("neural_ai.data.storage.implementations.parquet_storage.pl"):
            mock_df: MagicMock = MagicMock()
            mock_sorted: MagicMock = MagicMock()
            mock_df.sort.return_value = mock_sorted

            with patch.object(storage_service, "engine", "polars"):
                result = storage_service._sort_by_timestamp(mock_df)  # pyright: ignore[reportPrivateUsage]

                assert result == mock_sorted
                mock_df.sort.assert_called_once_with("timestamp")

    def test_sort_by_timestamp_pandas(self, storage_service: ParquetStorageService):
        """Teszteli a rendezést timestamp szerint Pandas esetén."""
        with patch("neural_ai.data.storage.implementations.parquet_storage.pd"):
            mock_df: MagicMock = MagicMock()
            mock_sorted: MagicMock = MagicMock()
            mock_df.sort_values.return_value.reset_index.return_value = mock_sorted

            with patch.object(storage_service, "engine", "fastparquet"):
                result = storage_service._sort_by_timestamp(mock_df)  # pyright: ignore[reportPrivateUsage]

                assert result == mock_sorted

    def test_filter_by_timestamp(self, storage_service: ParquetStorageService):
        """Teszteli az időbélyeg szerinti szűrést."""
        mock_df: MagicMock = MagicMock()
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2023, 12, 31)

        result = storage_service._filter_by_timestamp(mock_df, start_date, end_date)  # pyright: ignore[reportPrivateUsage]

        # A jelenlegi implementáció változatlanul visszaadja a DataFrame-et
        assert result == mock_df

    def test_read_parquet_async(self, storage_service: ParquetStorageService):
        """Teszteli az aszinkron Parquet olvasást."""
        mock_path: MagicMock = MagicMock()
        mock_result: MagicMock = MagicMock()

        storage_service.backend.read = MagicMock(return_value=mock_result)  # type: ignore[method-assign]

        async def run_test():
            result = await storage_service._read_parquet_async(mock_path)  # pyright: ignore[reportPrivateUsage]
            assert result == mock_result

        asyncio.run(run_test())

    # StorageInterface tesztek

    def test_save_dataframe(self, storage_service: ParquetStorageService):
        """Teszteli a DataFrame mentését StorageInterface-en keresztül."""
        mock_df: MagicMock = MagicMock()

        # The current implementation raises NotImplementedError
        with pytest.raises(NotImplementedError):
            storage_service.save_dataframe(  # pyright: ignore[reportUnknownMemberType]
                mock_df, "test_path", date=datetime(2023, 12, 23), symbol="EURUSD"
            )

    def test_load_dataframe(self, storage_service: ParquetStorageService):
        """Teszteli a DataFrame betöltését StorageInterface-en keresztül."""
        # The current implementation raises NotImplementedError
        with pytest.raises(NotImplementedError):
            storage_service.load_dataframe(  # pyright: ignore[reportUnknownMemberType]
                "test_path",
                start_date=datetime(2023, 12, 1),
                end_date=datetime(2023, 12, 31),
                symbol="EURUSD",
            )

    def test_exists(self, storage_service: ParquetStorageService, temp_dir: Path):
        """Teszteli az útvonal létezésének ellenőrzését."""
        test_file = temp_dir / "test_file.txt"
        test_file.write_text("content")

        assert storage_service.exists("test_file.txt")
        assert not storage_service.exists("nonexistent.txt")

    def test_get_metadata(self, storage_service: ParquetStorageService, temp_dir: Path):
        """Teszteli a fájl metaadatainak lekérdezését."""
        test_file = temp_dir / "test_file.txt"
        test_file.write_text("content")

        metadata = storage_service.get_metadata("test_file.txt")

        assert "size" in metadata
        assert "created" in metadata
        assert "modified" in metadata
        assert "accessed" in metadata
        assert metadata["is_file"] is True
        assert metadata["is_dir"] is False

    def test_delete_file(self, storage_service: ParquetStorageService, temp_dir: Path):
        """Teszteli a fájl törlését."""
        test_file = temp_dir / "test_file.txt"
        test_file.write_text("content")

        storage_service.delete("test_file.txt")

        assert not test_file.exists()

    def test_delete_directory(self, storage_service: ParquetStorageService, temp_dir: Path):
        """Teszteli a könyvtár törlését."""
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        storage_service.delete("test_dir")

        assert not test_dir.exists()

    def test_list_dir(self, storage_service: ParquetStorageService, temp_dir: Path):
        """Teszteli a könyvtár tartalmának listázását."""
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")

        files = storage_service.list_dir("test_dir")

        assert len(files) == 2
        assert all(isinstance(f, Path) for f in files)
