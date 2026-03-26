"""Tesztek a neural_ai.processors.dimensions.d02_support.__init__ modulhoz."""

import neural_ai.processors.dimensions.d02_support as d02_support


class TestD02SupportInit:
    """Tesztek a d02_support modul inicializálásához."""

    def test_module_exists(self) -> None:
        """Teszteli, hogy a modul létezik."""
        assert d02_support is not None

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert d02_support.__doc__ is not None
