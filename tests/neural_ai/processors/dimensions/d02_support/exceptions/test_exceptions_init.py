"""Tesztek a neural_ai.processors.dimensions.d02_support.exceptions.__init__ modulhoz."""

import neural_ai.processors.dimensions.d02_support.exceptions as exceptions


class TestD02SupportExceptionsInit:
    """Tesztek a d02_support.exceptions modul inicializálásához."""

    def test_module_exists(self) -> None:
        """Teszteli, hogy a modul létezik."""
        assert exceptions is not None

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert exceptions.__doc__ is not None
