"""PolarsBackend tesztjei."""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.storage.backends.polars_backend import PolarsBackend


class MockPolarsDataFrame:
    """Mock Polars DataFrame osztály."""

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

    def columns(self) -> list[str]:
        return list(self._data.keys())

    def shape(self) -> tuple[int, int]:
        return (len(self), len(self.columns()))

    def write_parquet(self, path: str, **kwargs):
        """Mock Parquet írás."""
        pass


class MockBatch:
    """Mock batch."""

    pass


class MockPyArrowParquet:
    """Mock PyArrow Parquet osztály."""

    class ParquetFile:
        def __init__(self, path: str):
            self.path = path
            self.metadata = MockMetadata()

        def iter_batches(self, batch_size: int = None, columns: list = None, filters: list = None):
            """Mock batch iterátor."""
            yield MockBatch()


class MockMetadata:
    """Mock metadata."""

    def __init__(self):
        self.num_rows = 100
        self.num_row_groups = 1
        self.schema = MockSchema()

    def row_group(self, index: int):
        return MockRowGroup()


class MockSchema:
    """Mock schema."""

    def __init__(self):
        self.names = ["timestamp", "symbol", "bid", "ask", "volume", "source"]


class MockRowGroup:
    """Mock row group."""

    def __init__(self):
        pass

    def column(self, index: int):
        return MockColumn()


class MockColumn:
    """Mock column."""

    def __init__(self):
        self.compression = "snappy"


@pytest.fixture
def mock_polars():
    """Polars mock fixture."""
    mock_pl = MagicMock()
    mock_pl.DataFrame = MockPolarsDataFrame
    mock_pl.read_parquet = MagicMock(return_value=MockPolarsDataFrame())
    mock_pl.concat = MagicMock(return_value=MockPolarsDataFrame())
    mock_pl.from_arrow = MagicMock(return_value=MockPolarsDataFrame())
    return mock_pl


@pytest.fixture
def mock_pyarrow():
    """PyArrow mock fixture."""
    mock_pa = MagicMock()
    mock_pq = MockPyArrowParquet()
    return mock_pa, mock_pq


@pytest.fixture
def backend(mock_polars, mock_pyarrow):
    """Backend fixture mock könyvtárakkal."""
    with (
        patch("neural_ai.core.storage.backends.polars_backend.polars", mock_polars),
        patch("neural_ai.core.storage.backends.polars_backend.pyarrow", mock_pyarrow[0]),
        patch("neural_ai.core.storage.backends.polars_backend.pq", mock_pyarrow[1]),
    ):
        backend = PolarsBackend()
        backend._initialized = True
        backend._polars_wrapper._polars = mock_polars
        backend._polars_wrapper._pyarrow = mock_pyarrow[0]
        backend._polars_wrapper._parquet = mock_pyarrow[1]
        yield backend


class TestPolarsBackend:
    """PolarsBackend osztály tesztjei."""

    def test_initialization(self, backend):
        """Teszteli a backend inicializálását."""
        assert backend.name == "polars"
        assert backend.supported_formats == ["parquet"]
        assert backend.is_async is True
        assert backend._initialized is True

    def test_lazy_import(self):
        """Teszteli a lazy import működését."""
        backend = PolarsBackend()

        # Kezdetben nincs betöltve
        assert backend._initialized is False
        assert backend._polars_wrapper._polars is None

    def test_write_success(self, backend, tmp_path):
        """Teszteli a sikeres írási műveletet."""
        data = MockPolarsDataFrame()
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
        data = MockPolarsDataFrame()

        # Nem Parquet kiterjesztés
        with pytest.raises(ValueError, match=".parquet kiterjesztéssel kell rendelkeznie"):
            backend.write(data, "test.csv")

    def test_read_success(self, backend, tmp_path):
        """Teszteli a sikeres olvasási műveletet."""
        data = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        # Először írunk
        backend.write(data, str(path))

        # Utána olvasunk
        result = backend.read(str(path))

        assert result is not None
        assert isinstance(result, MockPolarsDataFrame)

    def test_read_file_not_found(self, backend, tmp_path):
        """Teszteli a nem létező fájl olvasását."""
        path = tmp_path / "nonexistent.parquet"

        with pytest.raises(FileNotFoundError, match="A forrásfájl nem található"):
            backend.read(str(path))

    def test_read_with_columns(self, backend, tmp_path):
        """Teszteli az olvasást oszlopok szűrésével."""
        data = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        backend.write(data, str(path))
        result = backend.read(str(path), columns=["timestamp", "bid", "ask"])

        assert result is not None

    def test_read_with_filters(self, backend, tmp_path):
        """Teszteli az olvasást szűrőkkel."""
        data = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        backend.write(data, str(path))
        filters = [("year", "=", 2023)]
        result = backend.read(str(path), filters=filters)

        assert result is not None

    def test_read_chunked(self, backend, tmp_path):
        """Teszteli a chunkolt olvasást."""
        data = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        backend.write(data, str(path))
        result = backend.read(str(path), chunk_size=100)

        assert result is not None

    def test_append_success(self, backend, tmp_path):
        """Teszteli a sikeres hozzáfűzési műveletet."""
        data1 = MockPolarsDataFrame()
        data2 = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        # Először írunk
        backend.write(data1, str(path))

        # Utána hozzáfűzünk
        backend.append(data2, str(path))

        assert path.exists()

    def test_append_new_file(self, backend, tmp_path):
        """Teszteli a hozzáfűzést új fájlhoz."""
        data = MockPolarsDataFrame()
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
        data1 = MockPolarsDataFrame()
        data2 = MockPolarsDataFrame()
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
        data = MockPolarsDataFrame()
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
        existing = MockPolarsDataFrame()
        new = MockPolarsDataFrame()

        assert backend._validate_schema(existing, new) is True

    def test_validate_schema_incompatible(self, backend):
        """Teszteli az inkompatibilis sémák validálását."""
        existing = MockPolarsDataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        new = MockPolarsDataFrame({"col1": [3, 4]})  # Hiányzik a col2

        assert backend._validate_schema(existing, new) is False

    def test_write_with_compression(self, backend, tmp_path):
        """Teszteli az írást tömörítéssel."""
        data = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        backend.write(data, str(path), compression="snappy")

        assert path.exists()

    def test_write_with_partition_by(self, backend, tmp_path):
        """Teszteli az írást particionálással."""
        data = MockPolarsDataFrame()
        path = tmp_path / "test.parquet"

        backend.write(data, str(path), partition_by=["symbol"])

        assert path.parent.exists()

    def test_repr(self, backend):
        """Teszteli a backend szöveges reprezentációját."""
        repr_str = repr(backend)

        assert "PolarsBackend" in repr_str
        assert "polars" in repr_str
        assert "parquet" in repr_str
