"""Unit tesztek a neural_ai.core.logger.implementations.__init__ modulhoz."""

import neural_ai.core.logger.implementations as implementations_module


class TestLoggerImplementationsInit:
    """Tesztek a neural_ai.core.logger.implementations.__init__ modulhoz."""

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert implementations_module.__doc__ is not None
        assert len(implementations_module.__doc__) > 0

    def test_module_docstring_contains_warning(self) -> None:
        """Teszteli, hogy a docstring tartalmaz figyelmeztetést."""
        assert implementations_module.__doc__ is not None
        assert "ÜRES" in implementations_module.__doc__
        assert "factory.py" in implementations_module.__doc__

    def test_module_has_no_all_attribute(self) -> None:
        """Teszteli, hogy a modul nem rendelkezik __all__ attribútummal."""
        assert not hasattr(implementations_module, "__all__")

    def test_module_has_implementation_modules(self) -> None:
        """Teszteli, hogy a modul tartalmazza az implementációs modulokat."""
        # A Python automatikusan importálja a mappában lévő modulokat
        assert hasattr(implementations_module, "colored_logger")
        assert hasattr(implementations_module, "default_logger")
        assert hasattr(implementations_module, "rotating_file_logger")

    def test_module_docstring_mentions_implementations(self) -> None:
        """Teszteli, hogy a docstring említi az implementációkat."""
        assert implementations_module.__doc__ is not None
        assert "implementáció" in implementations_module.__doc__.lower()
