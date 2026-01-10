"""D01PriceFactory unit tesztek."""

from neural_ai.core.processing.dimensions.d01_price.factory import D01PriceFactory
from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor
from neural_ai.core.processing.interfaces.dimension_processor_interface import IDimensionProcessor


class TestD01PriceFactory:
    """D01PriceFactory unit teszt osztály."""

    def test_create_returns_correct_type(self):
        """Teszteli, hogy a create metódus helyes típust ad vissza."""
        processor = D01PriceFactory.create()

        assert isinstance(processor, D01PriceProcessor)
        assert isinstance(processor, IDimensionProcessor)

    def test_create_returns_new_instance(self):
        """Teszteli, hogy minden create hívás új példányt ad."""
        processor1 = D01PriceFactory.create()
        processor2 = D01PriceFactory.create()

        assert processor1 is not processor2
        assert isinstance(processor1, D01PriceProcessor)
        assert isinstance(processor2, D01PriceProcessor)

    def test_created_processor_has_correct_dimension_id(self):
        """Teszteli, hogy a létrehozott processor helyes dimension_id-val rendelkezik."""
        processor = D01PriceFactory.create()

        assert processor.dimension_id == 1

    def test_created_processor_is_functional(self):
        """Teszteli, hogy a létrehozott processor működőképes."""
        from datetime import datetime

        import polars as pl

        processor = D01PriceFactory.create()

        # Egyszerű teszt DataFrame
        test_df = pl.DataFrame(
            {
                "timestamp": [datetime(2023, 1, 1, 9, 0, 0)],
                "open": [1.0500],
                "high": [1.0520],
                "low": [1.0480],
                "close": [1.0510],
                "tick_volume": [1000],
                "spread": [0.0002],
                "real_volume": [1500.0],
            }
        )

        result = processor.process(test_df)

        assert isinstance(result, pl.DataFrame)
        assert len(result) == 1
        expected_columns = {
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "spread",
            "real_volume",
        }
        assert set(result.columns) == expected_columns
