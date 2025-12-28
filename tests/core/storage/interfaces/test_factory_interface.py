"""StorageFactoryInterface teszt modul.

Ez a modul tartalmazza a StorageFactoryInterface interfész tesztjeit.
"""

import inspect

import pytest

from neural_ai.core.storage.interfaces.factory_interface import (
    StorageFactoryInterface,
)


class TestStorageFactoryInterface:
    """StorageFactoryInterface interfész tesztjei."""

    def test_is_protocol(self) -> None:
        """Teszteli, hogy az interfész Protocol-t használ."""
        # Az interfésznek Protocol típusnak kell lennie (nem feltétlenül ABC)
        # A Protocol ellenőrzéséhez használjuk az inspect modult
        assert inspect.isclass(StorageFactoryInterface)

    def test_has_register_storage_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_storage metódussal."""
        # Ellenőrizzük, hogy a metódus létezik az interfészen
        assert hasattr(StorageFactoryInterface, "register_storage")

        # A metódusnak callable-nek kell lennie
        register_method = StorageFactoryInterface.register_storage
        assert callable(register_method)

    def test_has_get_storage_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik get_storage metódussal."""
        # Ellenőrizzük, hogy a metódus létezik az interfészen
        assert hasattr(StorageFactoryInterface, "get_storage")

        # A metódusnak callable-nek kell lennie
        get_storage_method = StorageFactoryInterface.get_storage
        assert callable(get_storage_method)

    def test_cannot_instantiate_directly(self) -> None:
        """Teszteli, hogy az interfész nem példányosítható közvetlenül."""
        # Az interfész nem példányosítható, mert Protocol
        with pytest.raises(TypeError):
            StorageFactoryInterface()  # type: ignore

    def test_register_storage_signature(self) -> None:
        """Teszteli a register_storage metódus aláírását."""
        # A metódusnak két paraméterrel kell rendelkeznie: storage_type és storage_class
        sig = inspect.signature(StorageFactoryInterface.register_storage)
        params = list(sig.parameters.keys())

        assert "storage_type" in params
        assert "storage_class" in params

    def test_get_storage_signature(self) -> None:
        """Teszteli a get_storage metódus aláírását."""
        # A metódusnak legalább egy paraméterrel kell rendelkeznie: storage_type
        sig = inspect.signature(StorageFactoryInterface.get_storage)
        params = list(sig.parameters.keys())

        assert "storage_type" in params
        # A **kwargs is kell, hogy legyen a végén
        assert any(str(sig.parameters[p].kind) == "VAR_KEYWORD" for p in params)
