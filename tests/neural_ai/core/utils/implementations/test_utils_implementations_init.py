"""Unit tesztek a neural_ai.core.utils.implementations.__init__ modulhoz."""

import neural_ai.core.utils.implementations as implementations_module


class TestUtilsImplementationsInit:
    """Tesztek a utils implementations __init__.py modulhoz."""

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert implementations_module.__doc__ is not None
        assert len(implementations_module.__doc__) > 0

    def test_docstring_contains_warning(self) -> None:
        """Teszteli, hogy a docstring tartalmaz figyelmeztetést."""
        assert implementations_module.__doc__ is not None
        assert "FIGYELEM" in implementations_module.__doc__
        assert "ÜRES" in implementations_module.__doc__

    def test_module_no_all(self) -> None:
        """Teszteli, hogy a modul nem rendelkezik __all__ attribútummal."""
        assert not hasattr(implementations_module, "__all__")

    def test_module_is_empty(self) -> None:
        """Teszteli, hogy a modul üres (csak docstring van)."""
        public_attrs = [
            name
            for name in dir(implementations_module)
            if not name.startswith("_")
        ]
        # A hardware_info modul automatikusan importálódik
        # de ez nem számít "export"-nak, mert nincs __all__
        assert len(public_attrs) <= 1  # Csak hardware_info lehet

    def test_docstring_mentions_factory(self) -> None:
        """Teszteli, hogy a docstring említi a factory-t."""
        assert implementations_module.__doc__ is not None
        assert "factory" in implementations_module.__doc__.lower()
