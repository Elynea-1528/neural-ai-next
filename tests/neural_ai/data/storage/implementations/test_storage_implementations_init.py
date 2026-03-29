"""Unit tesztek a neural_ai.data.storage.implementations.__init__ modulhoz."""

import neural_ai.data.storage.implementations as implementations_module


class TestStorageImplementationsInit:
    """Tesztek a storage implementations __init__.py modulhoz."""

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert implementations_module.__doc__ is not None
        assert len(implementations_module.__doc__) > 0

    def test_docstring_contains_warning(self) -> None:
        """Teszteli, hogy a docstring tartalmaz figyelmeztetést."""
        assert implementations_module.__doc__ is not None
        assert "REJTETT" in implementations_module.__doc__
        assert "Ne importálj innen" in implementations_module.__doc__

    def test_module_no_all(self) -> None:
        """Teszteli, hogy a modul nem rendelkezik __all__ attribútummal."""
        assert not hasattr(implementations_module, "__all__")

    def test_module_has_implementation_modules(self) -> None:
        """Teszteli, hogy a modul tartalmazza az implementációs modulokat."""
        # A Python automatikusan importálja a mappában lévő modulokat
        assert hasattr(implementations_module, "file_storage")
        assert hasattr(implementations_module, "parquet_storage")

    def test_docstring_mentions_factory(self) -> None:
        """Teszteli, hogy a docstring említi a factory-t."""
        assert implementations_module.__doc__ is not None
        assert "factory" in implementations_module.__doc__.lower()
