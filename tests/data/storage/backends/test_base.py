"""Storage Backend Base modul tesztelése.

Ez a modul tartalmazza a StorageBackend és DataFrameProtocol tesztjeit.
"""

from unittest.mock import Mock

import pytest

from neural_ai.data.storage.backends.base import DataFrameProtocol, StorageBackend


class TestDataFrameProtocol:
    """DataFrameProtocol tesztjei."""

    def test_protocol_has_required_members(self) -> None:
        """Teszteli, hogy a protokoll rendelkezik a szükséges tagokkal."""
        assert hasattr(DataFrameProtocol, "columns")
        assert hasattr(DataFrameProtocol, "__len__")


class TestStorageBackend:
    """StorageBackend absztrakt osztály tesztjei."""

    def test_backend_is_abstract(self) -> None:
        """Teszteli, hogy az osztály absztrakt-e."""
        with pytest.raises(TypeError):
            StorageBackend("test", ["parquet"])  # type: ignore

    def test_backend_initialization(self) -> None:
        """Teszteli a backend inicializálását mock implementációval."""

        class MockBackend(StorageBackend):
            """Mock backend implementáció."""

            def write(self, data, path, **kwargs):
                pass

            def read(self, path, **kwargs):
                return Mock()

            def append(self, data, path, **kwargs):
                pass

            def supports_format(self, format_name):
                return format_name in self.supported_formats

            def get_info(self, path):
                return {
                    "size": 1000,
                    "rows": 100,
                    "columns": ["col1", "col2"],
                    "format": "parquet",
                    "created": "2023-01-01",
                    "modified": "2023-01-02",
                }

        backend = MockBackend("test_backend", ["parquet", "csv"])

        assert backend.name == "test_backend"
        assert backend.supported_formats == ["parquet", "csv"]
        assert backend.is_async is True

    def test_validate_data_method(self) -> None:
        """Teszteli a validate_data metódust."""

        class MockBackend(StorageBackend):
            """Mock backend implementáció."""

            def write(self, data, path, **kwargs):
                pass

            def read(self, path, **kwargs):
                return Mock()

            def append(self, data, path, **kwargs):
                pass

            def supports_format(self, format_name):
                return True

            def get_info(self, path):
                return {}

        backend = MockBackend("test", ["parquet"])

        # Teszt: None adat
        assert not backend.validate_data(None)

        # Teszt: Érvénytelen adat (negatív hossz)
        mock_invalid = Mock()
        mock_invalid.__len__ = Mock(return_value=-1)
        assert not backend.validate_data(mock_invalid)

        # Teszt: Érvénytelen adat (nincs oszlop)
        mock_no_columns = Mock()
        mock_no_columns.__len__ = Mock(return_value=10)
        del mock_no_columns.columns
        assert not backend.validate_data(mock_no_columns)

        # Teszt: Érvényes adat - oszlopok mint attribútum
        mock_valid_attr = Mock()
        mock_valid_attr.__len__ = Mock(return_value=10)
        mock_valid_attr.columns = ["col1", "col2"]
        assert backend.validate_data(mock_valid_attr)

        # Teszt: Érvényes adat - oszlopok mint metódus
        mock_valid_method = Mock()
        mock_valid_method.__len__ = Mock(return_value=10)
        mock_valid_method.columns = Mock(return_value=["col1", "col2"])
        assert backend.validate_data(mock_valid_method)

        # Teszt: Üres oszloplista
        mock_empty_columns = Mock()
        mock_empty_columns.__len__ = Mock(return_value=10)
        mock_empty_columns.columns = []
        assert not backend.validate_data(mock_empty_columns)

        # Teszt: Kivétel kezelése
        mock_exception = Mock()
        mock_exception.__len__ = Mock(side_effect=Exception("Test exception"))
        assert not backend.validate_data(mock_exception)

    def test_supports_format_method(self) -> None:
        """Teszteli a supports_format metódust."""

        class MockBackend(StorageBackend):
            """Mock backend implementáció."""

            def write(self, data, path, **kwargs):
                pass

            def read(self, path, **kwargs):
                return Mock()

            def append(self, data, path, **kwargs):
                pass

            def supports_format(self, format_name):
                return format_name in self.supported_formats

            def get_info(self, path):
                return {}

        backend = MockBackend("test", ["parquet", "csv"])

        assert backend.supports_format("parquet")
        assert backend.supports_format("csv")
        assert not backend.supports_format("json")

    def test_repr_method(self) -> None:
        """Teszteli a __repr__ metódust."""

        class MockBackend(StorageBackend):
            """Mock backend implementáció."""

            def write(self, data, path, **kwargs):
                pass

            def read(self, path, **kwargs):
                return Mock()

            def append(self, data, path, **kwargs):
                pass

            def supports_format(self, format_name):
                return True

            def get_info(self, path):
                return {}

        backend = MockBackend("test_backend", ["parquet"])
        repr_str = repr(backend)

        assert "MockBackend" in repr_str
        assert "test_backend" in repr_str
        assert "parquet" in repr_str

    def test_all_abstract_methods_called(self) -> None:
        """Teszteli, hogy az összes absztrakt metódus meghívásra kerül."""

        class MockBackend(StorageBackend):
            """Mock backend implementáció."""

            def __init__(self):
                super().__init__("test", ["parquet"])
                self.write_called = False
                self.read_called = False
                self.append_called = False
                self.supports_format_called = False
                self.get_info_called = False

            def write(self, data, path, **kwargs):
                self.write_called = True

            def read(self, path, **kwargs):
                self.read_called = True
                return Mock()

            def append(self, data, path, **kwargs):
                self.append_called = True

            def supports_format(self, format_name):
                self.supports_format_called = True
                return True

            def get_info(self, path):
                self.get_info_called = True
                return {}

        backend = MockBackend()

        # Hívjuk meg az összes metódust
        backend.write(Mock(), "/test/path")
        backend.read("/test/path")
        backend.append(Mock(), "/test/path")
        backend.supports_format("parquet")
        backend.get_info("/test/path")

        # Ellenőrizzük, hogy mindegyik meghívásra került
        assert backend.write_called
        assert backend.read_called
        assert backend.append_called
        assert backend.supports_format_called
        assert backend.get_info_called

    def test_validate_data_edge_cases(self) -> None:
        """Teszteli a validate_data metódus szélsőséges eseteit."""

        class MockBackend(StorageBackend):
            """Mock backend implementáció."""

            def write(self, data, path, **kwargs):
                pass

            def read(self, path, **kwargs):
                return Mock()

            def append(self, data, path, **kwargs):
                pass

            def supports_format(self, format_name):
                return True

            def get_info(self, path):
                return {}

        backend = MockBackend("test", ["parquet"])

        # Teszt: 0 hosszúságú adat (nem negatív, de üres)
        mock_zero_length = Mock()
        mock_zero_length.__len__ = Mock(return_value=0)
        mock_zero_length.columns = ["col1"]
        assert not backend.validate_data(mock_zero_length)

        # Teszt: Oszlopok, de 0 hossz
        mock_columns_no_data = Mock()
        mock_columns_no_data.__len__ = Mock(return_value=0)
        mock_columns_no_data.columns = ["col1", "col2"]
        assert not backend.validate_data(mock_columns_no_data)

        # Teszt: Nincs oszlop, de van hossz
        mock_no_columns_with_length = Mock()
        mock_no_columns_with_length.__len__ = Mock(return_value=5)
        mock_no_columns_with_length.columns = []
        assert not backend.validate_data(mock_no_columns_with_length)

        # Teszt: Oszlop mint tuple
        mock_tuple_columns = Mock()
        mock_tuple_columns.__len__ = Mock(return_value=10)
        mock_tuple_columns.columns = ("col1", "col2")
        assert backend.validate_data(mock_tuple_columns)

        # Teszt: Oszlopok, de nincs __len__ metódusa
        mock_columns_no_len = Mock()
        mock_columns_no_len.columns = ["col1", "col2"]
        # Mivel a Mock-nak alapból van __len__ metódusa, explicit beállítjuk
        mock_columns_no_len.__len__ = Mock(return_value=10)
        assert backend.validate_data(mock_columns_no_len)
