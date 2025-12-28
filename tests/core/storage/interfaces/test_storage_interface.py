"""StorageInterface teszt modul.

Ez a modul tartalmazza a StorageInterface interfész tesztjeit.
"""

import inspect

import pytest

from neural_ai.core.storage.interfaces.storage_interface import (
    StorageInterface,
)


class TestStorageInterface:
    """StorageInterface interfész tesztjei."""

    def test_is_protocol(self) -> None:
        """Teszteli, hogy az interfész Protocol-t használ."""
        # Az interfésznek Protocol típusnak kell lennie (nem feltétlenül ABC)
        assert inspect.isclass(StorageInterface)

    def test_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik az összes szükséges metódussal."""
        required_methods = [
            "save_dataframe",
            "load_dataframe",
            "save_object",
            "load_object",
            "exists",
            "get_metadata",
            "delete",
            "list_dir",
        ]

        for method_name in required_methods:
            assert hasattr(StorageInterface, method_name), f"Missing method: {method_name}"

            # A metódusoknak callable-nek kell lenniük
            method = getattr(StorageInterface, method_name)
            assert callable(method), f"Method {method_name} should be callable"

    def test_cannot_instantiate_directly(self) -> None:
        """Teszteli, hogy az interfész nem példányosítható közvetlenül."""
        # Az interfész nem példányosítható, mert Protocol
        with pytest.raises(TypeError):
            StorageInterface()  # type: ignore

    def test_save_dataframe_signature(self) -> None:
        """Teszteli a save_dataframe metódus aláírását."""
        sig = inspect.signature(StorageInterface.save_dataframe)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "df" in params
        assert "path" in params

    def test_load_dataframe_signature(self) -> None:
        """Teszteli a load_dataframe metódus aláírását."""
        sig = inspect.signature(StorageInterface.load_dataframe)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "path" in params

    def test_save_object_signature(self) -> None:
        """Teszteli a save_object metódus aláírását."""
        sig = inspect.signature(StorageInterface.save_object)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "obj" in params
        assert "path" in params

    def test_load_object_signature(self) -> None:
        """Teszteli a load_object metódus aláírását."""
        sig = inspect.signature(StorageInterface.load_object)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "path" in params

    def test_exists_signature(self) -> None:
        """Teszteli az exists metódus aláírását."""
        sig = inspect.signature(StorageInterface.exists)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "path" in params

    def test_get_metadata_signature(self) -> None:
        """Teszteli a get_metadata metódus aláírását."""
        sig = inspect.signature(StorageInterface.get_metadata)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "path" in params

    def test_delete_signature(self) -> None:
        """Teszteli a delete metódus aláírását."""
        sig = inspect.signature(StorageInterface.delete)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "path" in params

    def test_list_dir_signature(self) -> None:
        """Teszteli a list_dir metódus aláírását."""
        sig = inspect.signature(StorageInterface.list_dir)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "path" in params
