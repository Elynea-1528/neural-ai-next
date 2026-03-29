"""Unit tesztek a neural_ai.data.storage.backends.__init__ modulhoz."""

import neural_ai.data.storage.backends as backends_module
from neural_ai.data.storage.backends.base import DataFrameType, StorageBackend
from neural_ai.data.storage.backends.pandas_backend import PandasBackend
from neural_ai.data.storage.backends.polars_backend import PolarsBackend


class TestStorageBackendsInit:
    """Tesztek a storage backends __init__.py modulhoz."""

    def test_module_has_all(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(backends_module, "__all__")
        assert isinstance(backends_module.__all__, list)

    def test_all_exports_dataframe_type(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a DataFrameType-ot."""
        assert "DataFrameType" in backends_module.__all__

    def test_all_exports_storage_backend(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a StorageBackend-et."""
        assert "StorageBackend" in backends_module.__all__

    def test_all_exports_pandas_backend(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a PandasBackend-et."""
        assert "PandasBackend" in backends_module.__all__

    def test_all_exports_polars_backend(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a PolarsBackend-et."""
        assert "PolarsBackend" in backends_module.__all__

    def test_dataframe_type_is_correct_class(self) -> None:
        """Teszteli, hogy a DataFrameType a helyes osztály."""
        assert backends_module.DataFrameType is DataFrameType

    def test_storage_backend_is_correct_class(self) -> None:
        """Teszteli, hogy a StorageBackend a helyes osztály."""
        assert backends_module.StorageBackend is StorageBackend

    def test_pandas_backend_is_correct_class(self) -> None:
        """Teszteli, hogy a PandasBackend a helyes osztály."""
        assert backends_module.PandasBackend is PandasBackend

    def test_polars_backend_is_correct_class(self) -> None:
        """Teszteli, hogy a PolarsBackend a helyes osztály."""
        assert backends_module.PolarsBackend is PolarsBackend

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert backends_module.__doc__ is not None
        assert len(backends_module.__doc__) > 0

    def test_docstring_mentions_backends(self) -> None:
        """Teszteli, hogy a docstring említi a backend-eket."""
        assert backends_module.__doc__ is not None
        assert "backend" in backends_module.__doc__.lower()

    def test_docstring_mentions_dataframe(self) -> None:
        """Teszteli, hogy a docstring említi a DataFrame-et."""
        assert backends_module.__doc__ is not None
        assert "dataframe" in backends_module.__doc__.lower()

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in backends_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_exist(self) -> None:
        """Teszteli, hogy az __all__-ban felsorolt elemek léteznek."""
        for name in backends_module.__all__:
            assert hasattr(backends_module, name)

    def test_storage_backend_is_abstract(self) -> None:
        """Teszteli, hogy a StorageBackend absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(backends_module.StorageBackend, ABCMeta)

    def test_pandas_backend_inherits_from_storage_backend(self) -> None:
        """Teszteli, hogy a PandasBackend a StorageBackend leszármazottja."""
        assert issubclass(backends_module.PandasBackend, backends_module.StorageBackend)

    def test_polars_backend_inherits_from_storage_backend(self) -> None:
        """Teszteli, hogy a PolarsBackend a StorageBackend leszármazottja."""
        assert issubclass(backends_module.PolarsBackend, backends_module.StorageBackend)

    def test_all_count(self) -> None:
        """Teszteli, hogy az __all__ 4 elemet tartalmaz."""
        assert len(backends_module.__all__) == 4
