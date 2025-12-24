"""StorageBackend absztrakt osztály tesztjei."""

from typing import Any

import pytest

from neural_ai.core.storage.backends.base import DataFrameType, StorageBackend


class MockDataFrame:
    """Mock DataFrame osztály a teszteléshez."""

    def __init__(self, data: dict[str, list] = None):
        self._data = data or {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}

    def __len__(self) -> int:
        """DataFrame hosszának lekérdezése."""
        return len(next(iter(self._data.values())))

    def columns(self) -> list[str]:
        """Oszlopok lekérdezése."""
        return list(self._data.keys())

    def shape(self) -> tuple[int, int]:
        """DataFrame alakjának lekérdezése."""
        return (len(self), len(self.columns()))


class ConcreteStorageBackend(StorageBackend):
    """Konkrét StorageBackend implementáció teszteléshez."""

    def __init__(self):
        super().__init__(name="test", supported_formats=["parquet", "csv"])
        self._written_data = {}
        self._files = {}

    def write(self, data: DataFrameType, path: str, **kwargs: dict[str, Any]) -> None:
        """Mock írási művelet."""
        if not self.validate_data(data):
            raise ValueError("Érvénytelen DataFrame adatok")
        self._written_data[path] = (data, kwargs)
        self._files[path] = {"exists": True}

    def read(self, path: str, **kwargs: dict[str, Any]) -> DataFrameType:
        """Mock olvasási művelet."""
        if path not in self._files:
            raise FileNotFoundError(f"A fájl nem található: {path}")
        data, _ = self._written_data.get(path, (MockDataFrame(), {}))
        return data

    def append(self, data: DataFrameType, path: str, **kwargs: dict[str, Any]) -> None:
        """Mock hozzáfűzési művelet."""
        if not self.validate_data(data):
            raise ValueError("Érvénytelen DataFrame adatok")

        if path in self._written_data:
            existing_data, _ = self._written_data[path]
            # Összefűzés (egyszerűsített)
            combined_data = MockDataFrame()
            self._written_data[path] = (combined_data, kwargs)
        else:
            self._written_data[path] = (data, kwargs)
            self._files[path] = {"exists": True}

    def supports_format(self, format_name: str) -> bool:
        """Formátum támogatás ellenőrzése."""
        return format_name.lower() in self.supported_formats

    def get_info(self, path: str) -> dict[str, Any]:
        """Mock fájl információ lekérdezés."""
        if path not in self._files:
            raise FileNotFoundError(f"A fájl nem található: {path}")

        data, _ = self._written_data.get(path, (MockDataFrame(), {}))
        return {
            "size": 1024,
            "rows": len(data),
            "columns": data.columns(),
            "format": "parquet",
            "created": "2023-01-01",
            "modified": "2023-01-01",
        }


class TestStorageBackend:
    """StorageBackend absztrakt osztály tesztjei."""

    def test_initialization(self):
        """Teszteli a backend inicializálását."""
        backend = ConcreteStorageBackend()

        assert backend.name == "test"
        assert backend.supported_formats == ["parquet", "csv"]
        assert backend.is_async is True

    def test_validate_data_valid(self):
        """Teszteli az érvényes adatok validálását."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()

        assert backend.validate_data(data) is True

    def test_validate_data_invalid(self):
        """Teszteli az érvénytelen adatok validálását."""
        backend = ConcreteStorageBackend()

        # Üres DataFrame
        empty_data = MockDataFrame({})
        assert backend.validate_data(empty_data) is False

        # None adatok
        assert backend.validate_data(None) is False

    def test_supports_format(self):
        """Teszteli a formátum támogatás ellenőrzését."""
        backend = ConcreteStorageBackend()

        assert backend.supports_format("parquet") is True
        assert backend.supports_format("csv") is True
        assert backend.supports_format("json") is False
        assert backend.supports_format("PARQUET") is True  # Case insensitive

    def test_repr(self):
        """Teszteli a backend szöveges reprezentációját."""
        backend = ConcreteStorageBackend()

        repr_str = repr(backend)
        assert "ConcreteStorageBackend" in repr_str
        assert "test" in repr_str
        assert "parquet" in repr_str

    def test_write_success(self):
        """Teszteli a sikeres írási műveletet."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()
        path = "test.parquet"

        # Sikeres írás
        backend.write(data, path)

        assert path in backend._written_data
        assert path in backend._files

    def test_write_invalid_data(self):
        """Teszteli az érvénytelen adatok írását."""
        backend = ConcreteStorageBackend()
        invalid_data = MockDataFrame({})  # Üres DataFrame

        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.write(invalid_data, "test.parquet")

    def test_read_success(self):
        """Teszteli a sikeres olvasási műveletet."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()
        path = "test.parquet"

        # Először írunk
        backend.write(data, path)

        # Utána olvasunk
        result = backend.read(path)

        assert result is not None
        assert len(result) == len(data)
        assert result.columns() == data.columns()

    def test_read_file_not_found(self):
        """Teszteli a nem létező fájl olvasását."""
        backend = ConcreteStorageBackend()

        with pytest.raises(FileNotFoundError, match="A fájl nem található"):
            backend.read("nonexistent.parquet")

    def test_append_success(self):
        """Teszteli a sikeres hozzáfűzési műveletet."""
        backend = ConcreteStorageBackend()
        data1 = MockDataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        data2 = MockDataFrame({"col1": [3, 4], "col2": ["c", "d"]})
        path = "test.parquet"

        # Először írunk
        backend.write(data1, path)

        # Utána hozzáfűzünk
        backend.append(data2, path)

        assert path in backend._written_data

    def test_append_new_file(self):
        """Teszteli a hozzáfűzést új fájlhoz."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()
        path = "new.parquet"

        # Hozzáfűzés nem létező fájlhoz (létrehozza)
        backend.append(data, path)

        assert path in backend._written_data
        assert path in backend._files

    def test_append_invalid_data(self):
        """Teszteli az érvénytelen adatok hozzáfűzését."""
        backend = ConcreteStorageBackend()
        invalid_data = MockDataFrame({})  # Üres DataFrame
        path = "test.parquet"

        with pytest.raises(ValueError, match="Érvénytelen DataFrame adatok"):
            backend.append(invalid_data, path)

    def test_get_info_success(self):
        """Teszteli a sikeres fájl információ lekérdezést."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()
        path = "test.parquet"

        # Először írunk
        backend.write(data, path)

        # Utána lekérdezzük az információkat
        info = backend.get_info(path)

        assert "size" in info
        assert "rows" in info
        assert "columns" in info
        assert "format" in info
        assert info["rows"] == len(data)
        assert info["columns"] == data.columns()

    def test_get_info_file_not_found(self):
        """Teszteli a nem létező fájl információ lekérdezését."""
        backend = ConcreteStorageBackend()

        with pytest.raises(FileNotFoundError, match="A fájl nem található"):
            backend.get_info("nonexistent.parquet")

    def test_write_with_kwargs(self):
        """Teszteli az írást extra paraméterekkel."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()
        path = "test.parquet"

        # Írás extra paraméterekkel
        backend.write(data, path, compression="snappy", partition_by=["col1"])

        assert path in backend._written_data
        _, kwargs = backend._written_data[path]
        assert kwargs.get("compression") == "snappy"
        assert kwargs.get("partition_by") == ["col1"]

    def test_read_with_kwargs(self):
        """Teszteli az olvasást extra paraméterekkel."""
        backend = ConcreteStorageBackend()
        data = MockDataFrame()
        path = "test.parquet"

        # Először írunk
        backend.write(data, path)

        # Olvasás extra paraméterekkel
        result = backend.read(path, columns=["col1"], filters=[("col1", ">", 1)])

        assert result is not None


class TestDataFrameType:
    """DataFrameType protokoll tesztjei."""

    def test_dataframe_protocol(self):
        """Teszteli, hogy a MockDataFrame megfelel a DataFrameType protokollnak."""
        data = MockDataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})

        # Ellenőrizzük a protokoll metódusait
        assert hasattr(data, "__len__")
        assert hasattr(data, "columns")
        assert hasattr(data, "shape")

        # Ellenőrizzük a visszatérési értékeket
        assert len(data) == 3
        assert data.columns() == ["col1", "col2"]
        assert data.shape() == (3, 2)

    def test_dataframe_with_empty_data(self):
        """Teszteli a DataFrame-t üres adatokkal."""
        data = MockDataFrame({})

        assert len(data) == 0
        assert data.columns() == []
        assert data.shape() == (0, 0)
