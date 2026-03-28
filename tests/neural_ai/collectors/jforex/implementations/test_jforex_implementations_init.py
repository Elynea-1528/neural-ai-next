"""Unit tesztek a neural_ai.collectors.jforex.implementations.__init__ modulhoz."""

import neural_ai.collectors.jforex.implementations as implementations_module


class TestJForexImplementationsInit:
    """Tesztek a neural_ai.collectors.jforex.implementations.__init__ modulhoz."""

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert implementations_module.__doc__ is not None
        assert len(implementations_module.__doc__) > 0

    def test_module_docstring_contains_warning(self) -> None:
        """Teszteli, hogy a docstring tartalmaz figyelmeztetést."""
        assert implementations_module.__doc__ is not None
        assert "REJTETT" in implementations_module.__doc__
        assert "Ne importálj innen" in implementations_module.__doc__

    def test_module_has_no_all_attribute(self) -> None:
        """Teszteli, hogy a modul nem rendelkezik __all__ attribútummal."""
        assert not hasattr(implementations_module, "__all__")

    def test_module_is_empty(self) -> None:
        """Teszteli, hogy a modul üres (csak docstring van)."""
        public_attrs = [
            name
            for name in dir(implementations_module)
            if not name.startswith("_")
        ]
        assert len(public_attrs) == 0

    def test_module_docstring_mentions_factory(self) -> None:
        """Teszteli, hogy a docstring említi a factory-t."""
        assert implementations_module.__doc__ is not None
        assert "factory" in implementations_module.__doc__
