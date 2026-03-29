"""Unit tesztek a neural_ai.data.storage.interfaces.__init__ modulhoz."""

import neural_ai.data.storage.interfaces as interfaces_module
from neural_ai.data.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class TestStorageInterfacesInit:
    """Tesztek a storage interfaces __init__.py modulhoz."""

    def test_module_has_all(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(interfaces_module, "__all__")
        assert isinstance(interfaces_module.__all__, list)

    def test_all_exports_storage_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a StorageInterface-t."""
        assert "StorageInterface" in interfaces_module.__all__

    def test_all_exports_storage_factory_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a StorageFactoryInterface-t."""
        assert "StorageFactoryInterface" in interfaces_module.__all__

    def test_storage_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a StorageInterface a helyes osztály."""
        assert interfaces_module.StorageInterface is StorageInterface

    def test_storage_factory_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a StorageFactoryInterface a helyes osztály."""
        assert interfaces_module.StorageFactoryInterface is StorageFactoryInterface

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert interfaces_module.__doc__ is not None
        assert len(interfaces_module.__doc__) > 0

    def test_docstring_mentions_storage(self) -> None:
        """Teszteli, hogy a docstring említi a tárolást."""
        assert interfaces_module.__doc__ is not None
        assert "tárol" in interfaces_module.__doc__.lower()

    def test_docstring_mentions_interface(self) -> None:
        """Teszteli, hogy a docstring említi az interfészeket."""
        assert interfaces_module.__doc__ is not None
        assert "interfész" in interfaces_module.__doc__.lower()

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in interfaces_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_exist(self) -> None:
        """Teszteli, hogy az __all__-ban felsorolt elemek léteznek."""
        for name in interfaces_module.__all__:
            assert hasattr(interfaces_module, name)

    def test_storage_interface_is_abstract(self) -> None:
        """Teszteli, hogy a StorageInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(interfaces_module.StorageInterface, ABCMeta)

    def test_storage_factory_interface_is_abstract(self) -> None:
        """Teszteli, hogy a StorageFactoryInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(interfaces_module.StorageFactoryInterface, ABCMeta)

    def test_all_count(self) -> None:
        """Teszteli, hogy az __all__ 2 elemet tartalmaz."""
        assert len(interfaces_module.__all__) == 2
