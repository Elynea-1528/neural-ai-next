"""PandasBackend tesztjei."""

import os
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.storage.backends.base import DataFrameType
from neural_ai.core.storage.backends.pandas_backend import PandasBackend


class MockPandasDataFrame:
    """Mock Pandas DataFrame osztály."""
    
    def __init__(self, data: dict = None):
        self._data = data or {
            "timestamp": [datetime.now()],
            "symbol": ["EURUSD"],
            "bid": [1.1000],
            "ask": [1.1002],
            "volume": [1000],
            "source": ["jforex"],
        }
    
    def __len__(self) -> int:
        return len(next(iter(self._data.values())))
    
    @property
    def columns(self):
        """Oszlopok lekérdezése."""
        return list(self._data.keys())
    
    def shape(self) -> tuple[int, int]:
        return (len(self), len(self.columns))


class MockFastParquet:
    """Mock FastParquet osztály."""
    
    @staticmethod
    def write(path: str, df, **kwargs):
        """Mock Parquet írás."""
        pass
    
    class ParquetFile:
        def __init__(self, path: str):
            self.path = path
            self.row_groups = [MockRowGroup()]
        
        def to_pandas(self, columns=None, filters=None):
            """Mock DataFrame konverzió."""
            return MockPandasDataFrame()
        
        def iter_row_groups(self):
            """Mock row group iterátor."""
            yield MockParquetFile()
        
        @property
        def info(self):
            """Mock info property."""
            return {"compression": "snappy"}


class MockParquetFile:
    """Mock ParquetFile."""
    
    def to_pandas(self, columns=None, filters=None):
        """Mock DataFrame konverzió."""
        return MockPandasDataFrame()


class MockRowGroup:
    """Mock row group."""
    pass


@pytest.fixture
def mock_pandas():
    """Pandas mock fixture."""
    mock_pd = MagicMock()
    mock_pd.DataFrame = MockPandasDataFrame
    mock_pd.concat = MagicMock(return_value=MockPandasDataFrame())
    return mock_pd


@pytest.fixture
def mock_fastparquet():
    """FastParquet mock fixture."""
    return MockFastParquet()


@pytest.fixture
def backend(mock_pandas, mock_fastparquet):
    """Backend fixture mock könyvtárakkal."""
    with patch("neural_ai.core.storage.backends.pandas_backend.pandas", mock_pandas), \
         patch("neural_ai.core.storage.backends.pandas_backend.fastparquet", mock_fastparquet):
        backend = PandasBackend()
        backend._initialized = True
        backend._pandas_wrapper._pandas = mock_pandas
        backend._pandas_wrapper._fastparquet = mock_fastparquet
        yield backend


class TestPandasBackend:
    """PandasBackend osztály tesztjei."""
    
    def test_initialization(self, backend):
        """Teszteli a backend inicializálását."""
        assert backend.name == "pandas"
        assert backend.supported_formats == ["parquet"]
        assert backend.is_async is True
        assert backend._initialized is True
    
    def test_lazy_import(self):
        """Teszteli a lazy import működését."""
        backend = PandasBackend()
        
        # Kezdetben nincs betöltve
        assert backend._initialized is False
        assert backend._pandas_wrapper._pandas is None
    
    def test_write_success(self, backend, tmp_path):
        """Teszteli a sikeres írási műveletet."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        # Sikeres írás
        backend.write(data, str(path))
        
        # Ellenőrizzük, hogy a fájl létrejött-e
        assert path.parent.exists()
    
    def test_write_invalid_data(self, backend, tmp_path):
        """Teszteli az érvénytelen adatok írását."""
        path = tmp_path / "test.parquet"
        
        # None adatok
        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.write(None, str(path))
    
    def test_write_invalid_path(self, backend):
        """Teszteli az érvénytelen elérési úttal történő írást."""
        data = MockPandasDataFrame()
        
        # Nem Parquet kiterjesztés
        with pytest.raises(ValueError, match=".parquet kiterjesztéssel kell rendelkeznie"):
            backend.write(data, "test.csv")
    
    def test_read_success(self, backend, tmp_path):
        """Teszteli a sikeres olvasási műveletet."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        # Először írunk
        backend.write(data, str(path))
        
        # Utána olvasunk
        result = backend.read(str(path))
        
        assert result is not None
        assert isinstance(result, MockPandasDataFrame)
    
    def test_read_file_not_found(self, backend, tmp_path):
        """Teszteli a nem létező fájl olvasását."""
        path = tmp_path / "nonexistent.parquet"
        
        with pytest.raises(FileNotFoundError, match="A forrásfájl nem található"):
            backend.read(str(path))
    
    def test_read_with_columns(self, backend, tmp_path):
        """Teszteli az olvasást oszlopok szűrésével."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path))
        result = backend.read(str(path), columns=["timestamp", "bid", "ask"])
        
        assert result is not None
    
    def test_read_with_filters(self, backend, tmp_path):
        """Teszteli az olvasást szűrőkkel."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path))
        filters = [("year", "=", 2023)]
        result = backend.read(str(path), filters=filters)
        
        assert result is not None
    
    def test_read_chunked(self, backend, tmp_path):
        """Teszteli a chunkolt olvasást."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path))
        result = backend.read(str(path), chunk_size=100)
        
        assert result is not None
    
    def test_append_success(self, backend, tmp_path):
        """Teszteli a sikeres hozzáfűzési műveletet."""
        data1 = MockPandasDataFrame()
        data2 = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        # Először írunk
        backend.write(data1, str(path))
        
        # Utána hozzáfűzünk
        backend.append(data2, str(path))
        
        assert path.exists()
    
    def test_append_new_file(self, backend, tmp_path):
        """Teszteli a hozzáfűzést új fájlhoz."""
        data = MockPandasDataFrame()
        path = tmp_path / "new.parquet"
        
        # Hozzáfűzés nem létező fájlhoz
        backend.append(data, str(path))
        
        assert path.exists()
    
    def test_append_invalid_data(self, backend, tmp_path):
        """Teszteli az érvénytelen adatok hozzáfűzését."""
        path = tmp_path / "test.parquet"
        
        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.append(None, str(path))
    
    def test_append_with_schema_validation(self, backend, tmp_path):
        """Teszteli a hozzáfűzést sémavizsgálattal."""
        data1 = MockPandasDataFrame()
        data2 = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data1, str(path))
        backend.append(data2, str(path), schema_validation=True)
        
        assert path.exists()
    
    def test_supports_format(self, backend):
        """Teszteli a formátum támogatás ellenőrzését."""
        assert backend.supports_format("parquet") is True
        assert backend.supports_format("csv") is False
        assert backend.supports_format("json") is False
        assert backend.supports_format("PARQUET") is True
    
    def test_get_info_success(self, backend, tmp_path):
        """Teszteli a sikeres fájl információ lekérdezést."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path))
        info = backend.get_info(str(path))
        
        assert "size" in info
        assert "rows" in info
        assert "columns" in info
        assert "format" in info
        assert "created" in info
        assert "modified" in info
        assert info["format"] == "parquet"
    
    def test_get_info_file_not_found(self, backend, tmp_path):
        """Teszteli a nem létező fájl információ lekérdezését."""
        path = tmp_path / "nonexistent.parquet"
        
        with pytest.raises(FileNotFoundError, match="A fájl nem található"):
            backend.get_info(str(path))
    
    def test_validate_schema_compatible(self, backend):
        """Teszteli a kompatibilis sémák validálását."""
        existing = MockPandasDataFrame()
        new = MockPandasDataFrame()
        
        assert backend._validate_schema(existing, new) is True
    
    def test_validate_schema_incompatible(self, backend):
        """Teszteli az inkompatibilis sémák validálását."""
        existing = MockPandasDataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        new = MockPandasDataFrame({"col1": [3, 4]})  # Hiányzik a col2
        
        assert backend._validate_schema(existing, new) is False
    
    def test_write_with_compression(self, backend, tmp_path):
        """Teszteli az írást tömörítéssel."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path), compression="snappy")
        
        assert path.exists()
    
    def test_write_with_partition_by(self, backend, tmp_path):
        """Teszteli az írást particionálással."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path), partition_by=["symbol"])
        
        assert path.parent.exists()
    
    def test_write_with_index(self, backend, tmp_path):
        """Teszteli az írást index mentésével."""
        data = MockPandasDataFrame()
        path = tmp_path / "test.parquet"
        
        backend.write(data, str(path), index=True)
        
        assert path.exists()
    
    def test_repr(self, backend):
        """Teszteli a backend szöveges reprezentációját."""
        repr_str = repr(backend)
        
        assert "PandasBackend" in repr_str
        assert "pandas" in repr_str
        assert "parquet" in repr_str