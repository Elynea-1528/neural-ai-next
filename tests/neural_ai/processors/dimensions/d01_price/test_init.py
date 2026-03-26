"""Tesztek a neural_ai.processors.dimensions.d01_price.__init__ modulhoz."""

import neural_ai.processors.dimensions.d01_price as d01_price


class TestD01PriceInit:
    """Tesztek a d01_price modul inicializálásához."""

    def test_module_exists(self) -> None:
        """Teszteli, hogy a modul létezik."""
        assert d01_price is not None

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert d01_price.__doc__ is not None
