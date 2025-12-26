"""ParquetStorageService komprehenszív tesztjei.

Ez a modul tartalmazza a ParquetStorageService teljes tesztlefedettségét,
beleértve a backend választást, adattárolást, adatlekérdezést és hibakezelést.
A tesztek a DI szabályokat követik, mockolják a függőségeket.
"""

import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Generator
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.storage.backends.base import StorageBackend
from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface


class MockStorageBackend(StorageBackend):
    """Mock StorageBackend a teszteléshez."""

    def __init__(self, name: str = "mock") -> None:
        """Inicializálja a mock backend-et."""
        super().__init__(name, ["parquet"], True)
        self.write_called = False
        self.read_called = False
        self.read_return_value: Any = None
        self.engine: str = "mock"

    def write(self, data: Any, path: str, **kwargs: Any) -> None:
        """Mock írási művelet."""
        self.write_called = True
        # Hozzuk létre a fájlt a mock íráshoz
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text("mock parquet data")

    def read(self, path: str, **kwargs: Any) -> Any:
        """Mock olvasási művelet."""
        self.read_called = True
        if self.read_return_value is not None:
            return self.read_return_value
        
        # Csak akkor adjunk vissza adatot, ha a fájl létezik
        import polars as pl
        if Path(path).exists():
            return pl.DataFrame({
                "timestamp": [datetime.now()],
                "bid": [1.1000],
                "ask": [1.1002],
            })
        else:
            return pl.DataFrame()

    def append(self, data: Any, path: str, **kwargs: Any) -> None:
        """Mock hozzáfűzési művelet."""
        pass

    def supports_format(self, format_name: str) -> bool:
        """Formátum támogatás ellenőrzése."""
        return format_name.lower() in self.supported_formats

    def get_info(self, path: str) -> dict[str, Any]:
        """Mock fájl információ."""
        return {
            "size": 1024,
            "rows": 100,
            "columns": ["timestamp", "bid", "ask"],
            "format": "parquet",
            "created": datetime.now(),
            "modified": datetime.now(),
        }


@pytest.fixture
def mock_hardware_avx2() -> Mock:
    """Mock hardware interfész AVX2 támogatással."""
    hardware = Mock(spec=HardwareInterface)
    hardware.has_avx2 = Mock(return_value=True)
    return hardware


@pytest.fixture
def mock_hardware_no_avx2() -> Mock:
    """Mock hardware interfész AVX2 támogatás nélkül."""
    hardware = Mock(spec=HardwareInterface)
    hardware.has_avx2 = Mock(return_value=False)
    return hardware


@pytest.fixture
def mock_polars_backend() -> MockStorageBackend:
    """Mock PolarsBackend."""
    backend = MockStorageBackend("polars")
    backend.engine = "polars"
    return backend


@pytest.fixture
def mock_pandas_backend() -> MockStorageBackend:
    """Mock PandasBackend."""
    backend = MockStorageBackend("pandas")
    backend.engine = "fastparquet"
    return backend


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Átmeneti könyvtár létrehozása."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def service_avx2(
    temp_dir: Path, 
    mock_hardware_avx2: Mock, 
    mock_polars_backend: MockStorageBackend
) -> Generator[ParquetStorageService, None, None]:
    """ParquetStorageService AVX2 támogatással."""
    with patch('neural_ai.core.storage.backends.polars_backend.PolarsBackend') as mock_polars:
        mock_polars.return_value = mock_polars_backend
        service = ParquetStorageService(
            base_path=temp_dir,
            hardware=mock_hardware_avx2
        )
        service.backend = mock_polars_backend
        yield service


@pytest.fixture
def service_no_avx2(
    temp_dir: Path,
    mock_hardware_no_avx2: Mock, 
    mock_pandas_backend: MockStorageBackend
) -> Generator[ParquetStorageService, None, None]:
    """ParquetStorageService AVX2 támogatás nélkül."""
    with patch('neural_ai.core.storage.backends.pandas_backend.PandasBackend') as mock_pandas:
        mock_pandas.return_value = mock_pandas_backend
        service = ParquetStorageService(
            base_path=temp_dir,
            hardware=mock_hardware_no_avx2
        )
        service.backend = mock_pandas_backend
        yield service


class TestParquetStorageServiceInitialization:
    """ParquetStorageService inicializációs tesztjei."""

    def test_init_with_avx2(
        self, 
        temp_dir: Path, 
        mock_hardware_avx2: Mock, 
        mock_polars_backend: MockStorageBackend
    ) -> None:
        """Teszteli az inicializálást AVX2 támogatással."""
        with patch('neural_ai.core.storage.backends.polars_backend.PolarsBackend') as mock_polars:
            mock_polars.return_value = mock_polars_backend
            service = ParquetStorageService(
                base_path=temp_dir,
                hardware=mock_hardware_avx2
            )
            
            assert service.BASE_PATH == temp_dir
            assert service.compression == "snappy"
            assert service.engine == "polars"
            assert service.backend.name == "polars"

    def test_init_without_avx2(
        self,
        mock_hardware_no_avx2: Mock,
        mock_pandas_backend: MockStorageBackend
    ) -> None:
        """Teszteli az inicializálást AVX2 támogatás nélkül."""
        # A Singleton miatt törölni kell a korábbi példányt
        import neural_ai.core.storage.implementations.parquet_storage
        if hasattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance'):
            delattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance')
        
        with patch('neural_ai.core.storage.backends.pandas_backend.PandasBackend') as mock_pandas:
            mock_pandas.return_value = mock_pandas_backend
            service = ParquetStorageService(
                base_path="/test/path",
                hardware=mock_hardware_no_avx2
            )
            
            assert service.BASE_PATH == Path("/test/path")
            assert service.compression == "snappy"
            assert service.engine == "fastparquet"
            assert service.backend.name == "pandas"

    def test_init_default_path(
        self,
        mock_hardware_no_avx2: Mock,
        mock_pandas_backend: MockStorageBackend
    ) -> None:
        """Teszteli az alapértelmezett útvonal beállítását."""
        # A Singleton miatt törölni kell a korábbi példányt
        import neural_ai.core.storage.implementations.parquet_storage
        if hasattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance'):
            delattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance')
        
        with patch('neural_ai.core.storage.backends.pandas_backend.PandasBackend') as mock_pandas:
            mock_pandas.return_value = mock_pandas_backend
            service = ParquetStorageService(hardware=mock_hardware_no_avx2)
            
            assert service.BASE_PATH == Path("/data/tick")

    def test_init_custom_compression(
        self,
        mock_hardware_no_avx2: Mock,
        mock_pandas_backend: MockStorageBackend
    ) -> None:
        """Teszteli az egyéni tömörítés beállítását."""
        # A Singleton miatt törölni kell a korábbi példányt
        import neural_ai.core.storage.implementations.parquet_storage
        if hasattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance'):
            delattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance')
        
        with patch('neural_ai.core.storage.backends.pandas_backend.PandasBackend') as mock_pandas:
            mock_pandas.return_value = mock_pandas_backend
            service = ParquetStorageService(
                base_path="/test/path",
                compression="gzip",
                hardware=mock_hardware_no_avx2
            )
            
            assert service.compression == "gzip"


class TestParquetStorageServicePathGeneration:
    """Elérési út generálási tesztjei."""

    def test_get_path(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az elérési út generálását."""
        date = datetime(2023, 12, 23)
        path = service_avx2._get_path("EURUSD", date)
        
        expected = service_avx2.BASE_PATH / "EURUSD" / "tick" / "year=2023" / "month=12" / "day=23" / "data.parquet"
        assert path == expected

    def test_get_path_case_insensitive(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli a kis- és nagybetű érzéketlen szimbólumkezelést."""
        date = datetime(2023, 12, 23)
        path = service_avx2._get_path("eurusd", date)
        
        assert "EURUSD" in str(path)


class TestParquetStorageServiceStoreTickData:
    """Tick adatok tárolásának tesztjei."""

    @pytest.mark.asyncio
    async def test_store_tick_data_success(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli a sikeres tick adat tárolást."""
        import polars as pl
        mock_df = pl.DataFrame({
            "timestamp": [datetime.now()],
            "bid": [1.1000],
            "ask": [1.1002],
        })
        date = datetime(2023, 12, 23)
        
        await service_avx2.store_tick_data("EURUSD", mock_df, date)
        
        # Ellenőrizzük, hogy a backend write metódusa meghívódott
        assert service_avx2.backend.write_called

    @pytest.mark.asyncio
    async def test_store_tick_data_empty_dataframe(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az üres DataFrame tárolását."""
        import polars as pl
        mock_df = pl.DataFrame({"timestamp": [], "bid": [], "ask": []})
        date = datetime(2023, 12, 23)
        
        with pytest.raises(ValueError, match="Cannot store empty DataFrame"):
            await service_avx2.store_tick_data("EURUSD", mock_df, date)

    @pytest.mark.asyncio
    async def test_store_tick_data_missing_columns(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli a hiányzó oszlopokkal rendelkező DataFrame tárolását."""
        import polars as pl
        mock_df = pl.DataFrame({"timestamp": [datetime.now()]})  # Hiányzik bid és ask
        date = datetime(2023, 12, 23)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            await service_avx2.store_tick_data("EURUSD", mock_df, date)


class TestParquetStorageServiceReadTickData:
    """Tick adatok olvasásának tesztjei."""

    @pytest.mark.asyncio
    async def test_read_tick_data_no_files(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az olvasást, ha nincsenek fájlok."""
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2023, 12, 31)
        
        result = await service_avx2.read_tick_data("EURUSD", start_date, end_date)
        
        # Üres DataFrame-t kell kapjunk
        assert len(result) == 0


class TestParquetStorageServiceAvailableDates:
    """Elérhető dátumok lekérdezésének tesztjei."""

    @pytest.mark.asyncio
    async def test_get_available_dates_no_data(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az elérhető dátumok lekérdezését, ha nincs adat."""
        available_dates = await service_avx2.get_available_dates("EURUSD")
        
        assert len(available_dates) == 0


class TestParquetStorageServiceChecksum:
    """Checksum számítás tesztjei."""

    @pytest.mark.asyncio
    async def test_calculate_checksum_no_file(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli a checksum számítását, ha a fájl nem létezik."""
        date = datetime(2023, 12, 23)
        checksum = await service_avx2.calculate_checksum("EURUSD", date)
        
        assert checksum == ""


class TestParquetStorageServiceDataIntegrity:
    """Adatintegritás ellenőrzés tesztjei."""

    @pytest.mark.asyncio
    async def test_verify_data_integrity_no_file(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az adatintegritás ellenőrzést, ha a fájl nem létezik."""
        date = datetime(2023, 12, 23)
        is_valid = await service_avx2.verify_data_integrity("EURUSD", date)
        
        assert is_valid is False

    @pytest.mark.asyncio
    async def test_verify_data_integrity_missing_columns(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az adatintegritás ellenőrzést hiányzó oszlopokkal."""
        # Írjuk felül a backend read metódusát
        import polars as pl
        invalid_df = pl.DataFrame({"timestamp": [datetime.now()]})  # Hiányzik bid és ask
        service_avx2.backend.read = Mock(return_value=invalid_df)
        
        date = datetime(2023, 12, 23)
        is_valid = await service_avx2.verify_data_integrity("EURUSD", date)
        
        assert is_valid is False


class TestParquetStorageServiceStorageStats:
    """Tárolási statisztikák tesztjei."""

    @pytest.mark.asyncio
    async def test_get_storage_stats_no_data(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli a tárolási statisztikák lekérdezését, ha nincs adat."""
        stats = await service_avx2.get_storage_stats()
        
        assert stats["total_files"] == 0
        assert stats["total_size_gb"] == 0.0


class TestParquetStorageServiceBackendSelection:
    """Backend kiválasztás tesztjei."""

    def test_select_backend_avx2(
        self, 
        temp_dir: Path, 
        mock_hardware_avx2: Mock, 
        mock_polars_backend: MockStorageBackend
    ) -> None:
        """Teszteli a PolarsBackend kiválasztását AVX2 esetén."""
        with patch('neural_ai.core.storage.backends.polars_backend.PolarsBackend') as mock_polars:
            mock_polars.return_value = mock_polars_backend
            service = ParquetStorageService(
                base_path=temp_dir,
                hardware=mock_hardware_avx2
            )
            
            assert service.engine == "polars"
            assert service.backend.name == "polars"

    def test_select_backend_no_avx2(
        self,
        mock_hardware_no_avx2: Mock,
        mock_pandas_backend: MockStorageBackend
    ) -> None:
        """Teszteli a PandasBackend kiválasztását AVX2 hiányában."""
        # A Singleton miatt törölni kell a korábbi példányt
        import neural_ai.core.storage.implementations.parquet_storage
        if hasattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance'):
            delattr(neural_ai.core.storage.implementations.parquet_storage.ParquetStorageService, '_instance')
        
        with patch('neural_ai.core.storage.backends.pandas_backend.PandasBackend') as mock_pandas:
            mock_pandas.return_value = mock_pandas_backend
            service = ParquetStorageService(
                base_path="/test/path",
                hardware=mock_hardware_no_avx2
            )
            
            assert service.engine == "fastparquet"
            assert service.backend.name == "pandas"


class TestParquetStorageServiceAsyncOperations:
    """Aszinkron műveletek tesztjei."""

    @pytest.mark.asyncio
    async def test_concat_dataframes_polars(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli a DataFrame-ek összefűzését Polars esetén."""
        import polars as pl
        
        mock_dfs = [
            pl.DataFrame({"timestamp": [datetime.now()], "bid": [1.1000], "ask": [1.1002]}),
            pl.DataFrame({"timestamp": [datetime.now()], "bid": [1.1001], "ask": [1.1003]}),
        ]
        
        result = service_avx2._concat_dataframes(mock_dfs)
        
        assert result is not None
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_filter_by_timestamp_polars(self, service_avx2: ParquetStorageService) -> None:
        """Teszteli az időbélyeg szerinti szűrést Polars esetén."""
        import polars as pl
        
        mock_df = pl.DataFrame({
            "timestamp": [datetime(2023, 12, 15), datetime(2024, 1, 15)],
            "bid": [1.1000, 1.1001],
            "ask": [1.1002, 1.1003],
        })
        start_date = datetime(2023, 12, 1)
        end_date = datetime(2023, 12, 31)
        
        result = service_avx2._filter_by_timestamp(mock_df, start_date, end_date)
        
        assert result is not None
        assert len(result) == 1