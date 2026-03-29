"""Tesztek a neural_ai.processors.dimensions.d01_price.factory modulhoz."""

from neural_ai.processors.dimensions.d01_price.factory import D01PriceFactory


class TestD01PriceFactory:
    """Tesztek a D01PriceFactory osztályhoz."""

    def test_factory_exists(self) -> None:
        """Teszteli, hogy a factory osztály létezik."""
        assert D01PriceFactory is not None

    def test_factory_has_create_processor_method(self) -> None:
        """Teszteli, hogy a factory rendelkezik create_processor metódussal."""
        assert hasattr(D01PriceFactory, "create_processor")
